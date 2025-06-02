import sys
import json
from collections import defaultdict

def analyze_data(docs_json_str):
    try:
        all_docs_data = json.loads(docs_json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON input: {e}", file=sys.stderr)
        return {"error": "Invalid JSON input"}

    # Filter for relevant info-types
    relevant_docs = [
        doc for doc in all_docs_data
        if doc.get("info-type") in ["standard-definition", "policy-document"] and "error" not in doc
    ]

    # Create a lookup map for relevant docs by standard_id
    docs_by_id = {doc["standard_id"]: doc for doc in relevant_docs if doc.get("standard_id")}

    identified_pairs = set() # Use a set of frozensets to store pairs uniquely

    # Analyze related-standards for direct links
    for doc in relevant_docs:
        doc_id = doc.get("standard_id")
        if not doc_id:
            continue

        related_ids = doc.get("related-standards", [])
        if not isinstance(related_ids, list): # Should be list from previous script
            related_ids = []

        for rel_id_raw in related_ids:
            # Clean up potential wikilink format from related_id
            rel_id_cleaned = rel_id_raw.replace("[[", "").replace("]]", "")

            if rel_id_cleaned in docs_by_id:
                # Found a relevant related document
                # Add as a pair, ensuring smaller ID is first for uniqueness in the set
                pair = tuple(sorted((doc_id, rel_id_cleaned)))
                identified_pairs.add(pair)

    # Analyze for common ID prefixes (e.g., CS-POLICY- and AS- corresponding)
    # This is a more heuristic approach. Group by the first two parts of standard_id.
    # e.g. AS-KB-DIRECTORY-STRUCTURE -> AS-KB
    # e.g. CS-ADMONITIONS-POLICY -> CS-ADMONITIONS

    # Let's refine grouping:
    # Group by theme, often the middle part of an ID, e.g., "KB-ROOT" from AS-STRUCTURE-KB-ROOT and CS-POLICY-KB-ROOT
    # Or "ADMONITIONS" from CS-ADMONITIONS-POLICY and a hypothetical SF-ADMONITIONS-SYNTAX

    # For this task, the prompt asks for pairs of "Standard Definition" and "Policy Document".
    # A common pattern is AS-THEME and CS-POLICY-THEME or similar.

    # Let's try to find direct AS-xxx <-> CS-POLICY-xxx links first via the `identified_pairs`
    # Then, look for thematic links.

    # Thematic grouping based on "standard_id" parts
    # Example: AS-STRUCTURE-KB-ROOT and CS-POLICY-KB-ROOT
    # We can split by '-' and look for matching core themes.

    themed_groups = defaultdict(list)
    for doc_id in docs_by_id.keys():
        parts = doc_id.split('-')
        if len(parts) > 1: # AS-SOMETHING or CS-SOMETHING-ELSE
            theme_key_parts = []
            # For AS-TYPE-THEME, theme is THEME
            # For CS-POLICY-THEME, theme is THEME
            # For SF-SYNTAX-THEME, theme is THEME
            if parts[0] == "AS" and len(parts) > 2:
                theme_key_parts = parts[2:]
            elif parts[0] == "CS" and parts[1] == "POLICY" and len(parts) > 2:
                theme_key_parts = parts[2:]
            elif parts[0] == "SF" and len(parts) > 2: # Assuming SF-SYNTAX-THEME
                 theme_key_parts = parts[2:]

            if theme_key_parts:
                theme_key = "-".join(theme_key_parts)
                themed_groups[theme_key].append(doc_id)

    # Filter themed_groups to only include those with both a standard-definition and a policy-document
    final_themed_pairs = set()
    for theme, ids_in_theme in themed_groups.items():
        if len(ids_in_theme) > 1: # Need at least two to form a pair
            has_sd = False
            has_pd = False
            sd_id = None
            pd_id = None
            for doc_id_in_theme in ids_in_theme:
                doc_in_theme = docs_by_id.get(doc_id_in_theme)
                if doc_in_theme:
                    if doc_in_theme.get("info-type") == "standard-definition":
                        has_sd = True
                        sd_id = doc_id_in_theme
                    elif doc_in_theme.get("info-type") == "policy-document":
                        has_pd = True
                        pd_id = doc_id_in_theme

            if has_sd and has_pd and sd_id and pd_id:
                 # Add as a pair, ensuring smaller ID is first for uniqueness in the set
                pair = tuple(sorted((sd_id, pd_id)))
                identified_pairs.add(pair) # Add to the main identified_pairs set


    # Convert set of tuples to list of lists for JSON output
    identified_pairs_list = [list(pair) for pair in identified_pairs]

    return {
        "all_documents_processed_count": len(all_docs_data),
        "relevant_document_count_sd_pd": len(relevant_docs),
        "relevant_documents_details": relevant_docs, # Full details of relevant docs
        "identified_pairs_and_groups": identified_pairs_list
    }

if __name__ == '__main__':
    # Read from stdin
    input_json_str = sys.stdin.read()
    analysis_result = analyze_data(input_json_str)
    print(json.dumps(analysis_result, indent=2))
