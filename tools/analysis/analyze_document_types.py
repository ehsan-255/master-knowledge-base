#!/usr/bin/env python3
"""
On-Demand Document Type Analysis CLI

Implementation of Phase 1: Step 1.1.2 - Create On-Demand Analysis CLI
From: ultimate-frontmatter-enhancement-guideline-20250617-0312.md

This CLI provides on-demand document type analysis for both current repository
and future KB imports with comprehensive reporting.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from analysis.document_type_analyzer import UniversalDocumentTypeAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def setup_argument_parser():
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description='Universal Document Type Analyzer CLI',
        epilog="""
Examples:
  # Analyze current repository
  python tools/analysis/analyze_document_types.py --scan-current --output tools/reports/analysis-$(date +%%Y%%m%%d-%%H%%M).json

  # Analyze KB import
  python tools/analysis/analyze_document_types.py --kb-import-mode --source-path /path/to/new/kb --output tools/reports/kb-analysis-$(date +%%Y%%m%%d-%%H%%M).json

  # Analyze specific directories
  python tools/analysis/analyze_document_types.py --target-paths standards/ tools/ --output tools/reports/targeted-analysis-$(date +%%Y%%m%%d-%%H%%M).json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main operation modes
    parser.add_argument('--scan-current', action='store_true',
                       help='Analyze the current repository (default mode)')
    
    parser.add_argument('--kb-import-mode', action='store_true',
                       help='Enable KB import analysis mode')
    
    # Path specifications
    parser.add_argument('--source-path', type=str,
                       help='Path to analyze (for KB import mode)')
    
    parser.add_argument('--target-paths', nargs='+', type=str,
                       help='Specific paths to analyze (can specify multiple)')
    
    # Output configuration
    parser.add_argument('--output', type=str, required=True,
                       help='Output file path for analysis results (JSON format)')
    
    parser.add_argument('--report-format', choices=['json', 'markdown', 'both'], default='json',
                       help='Output format for analysis report')
    
    # Analysis configuration
    parser.add_argument('--include-shacl-profiles', action='store_true', default=True,
                       help='Include SHACL profile suggestions in output')
    
    parser.add_argument('--include-recommendations', action='store_true', default=True,
                       help='Include actionable recommendations in output')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    return parser


def validate_arguments(args):
    """Validate command line arguments."""
    errors = []
    
    # Validate operation mode
    if not args.scan_current and not args.kb_import_mode and not args.target_paths:
        args.scan_current = True  # Default to current repository scan
    
    if args.kb_import_mode and not args.source_path:
        errors.append("KB import mode requires --source-path to be specified")
    
    if args.source_path and not args.kb_import_mode:
        errors.append("--source-path can only be used with --kb-import-mode")
    
    # Validate paths
    if args.target_paths:
        for path in args.target_paths:
            if not Path(path).exists():
                errors.append(f"Target path does not exist: {path}")
    
    if args.source_path and not Path(args.source_path).exists():
        errors.append(f"Source path does not exist: {args.source_path}")
    
    # Validate output path
    output_dir = Path(args.output).parent
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created output directory: {output_dir}")
        except Exception as e:
            errors.append(f"Cannot create output directory {output_dir}: {e}")
    
    return errors


def run_analysis(args):
    """Run the document type analysis based on provided arguments."""
    logger.info("Starting Universal Document Type Analysis")
    
    # Initialize analyzer
    if args.kb_import_mode:
        analyzer = UniversalDocumentTypeAnalyzer(args.source_path)
        target_paths = [Path(args.source_path)]
    elif args.target_paths:
        analyzer = UniversalDocumentTypeAnalyzer()
        target_paths = [Path(p) for p in args.target_paths]
    else:
        # Default: scan current repository
        analyzer = UniversalDocumentTypeAnalyzer()
        target_paths = None
    
    # Run analysis
    try:
        logger.info(f"Analysis mode: {'KB Import' if args.kb_import_mode else 'Repository Scan'}")
        if target_paths:
            logger.info(f"Target paths: {[str(p) for p in target_paths]}")
        
        results = analyzer.analyze_on_demand(
            target_paths=target_paths,
            kb_import_mode=args.kb_import_mode
        )
        
        # Add metadata about this analysis run
        results['analysis_run_metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'cli_arguments': vars(args),
            'analyzer_version': '1.0.0',
            'analysis_mode': 'kb_import' if args.kb_import_mode else 'repository_scan'
        }
        
        logger.info(f"Analysis completed successfully")
        logger.info(f"Document types found: {len(results['document_types_identified'])}")
        logger.info(f"Total documents analyzed: {results['analysis_metadata']['total_documents_analyzed']}")
        
        return results
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise


def save_results(results, args):
    """Save analysis results in the specified format(s)."""
    output_path = Path(args.output)
    
    if args.report_format in ['json', 'both']:
        # Save JSON results
        json_path = output_path.with_suffix('.json') if output_path.suffix != '.json' else output_path
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"JSON results saved to: {json_path}")
        except Exception as e:
            logger.error(f"Failed to save JSON results: {e}")
            raise
    
    if args.report_format in ['markdown', 'both']:
        # Save Markdown report
        md_path = output_path.with_suffix('.md')
        try:
            markdown_content = generate_markdown_report(results)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            logger.info(f"Markdown report saved to: {md_path}")
        except Exception as e:
            logger.error(f"Failed to save Markdown report: {e}")
            raise


def generate_markdown_report(results):
    """Generate a markdown report from analysis results."""
    timestamp = results['analysis_run_metadata']['timestamp']
    analysis_mode = results['analysis_run_metadata']['analysis_mode']
    
    report = f"""# Document Type Analysis Report

**Generated:** {timestamp}  
**Analysis Mode:** {analysis_mode.replace('_', ' ').title()}  
**Analyzer:** Universal Document Type Analyzer v{results['analysis_run_metadata']['analyzer_version']}

---

## Executive Summary

- **Document Types Identified:** {len(results['document_types_identified'])}
- **Total Documents Analyzed:** {results['analysis_metadata']['total_documents_analyzed']}
- **Analysis Scope:** {', '.join(results['analysis_metadata']['target_paths'])}

## Document Type Breakdown

"""
    
    for doc_type, profile in results['document_types_identified'].items():
        file_count = len(profile['files'])
        report += f"""### {doc_type.replace('-', ' ').title()}

- **Files:** {file_count}
- **Mandatory Fields:** {', '.join(profile['field_requirements']['mandatory_fields'])}
- **Optional Fields:** {', '.join(profile['field_requirements']['optional_fields'])}
- **Forbidden Fields:** {', '.join(profile['field_requirements']['forbidden_fields'])}

"""
    
    # Add field usage matrix
    report += """## Field Usage Matrix

| Field | Usage Count | Common Values |
|-------|-------------|---------------|
"""
    
    for field, count in results['field_usage_matrix']['usage_counts'].items():
        values = results['field_usage_matrix']['value_patterns'].get(field, [])
        common_values = ', '.join(values[:3])  # Show first 3 values
        if len(values) > 3:
            common_values += f" (+{len(values) - 3} more)"
        report += f"| `{field}` | {count} | {common_values} |\n"
    
    # Add recommendations
    if results.get('recommended_actions'):
        report += """
## Recommended Actions

"""
        for i, action in enumerate(results['recommended_actions'], 1):
            report += f"""### {i}. {action['action'].replace('_', ' ').title()}

**Priority:** {action['priority'].title()}  
**Description:** {action['description']}  
**Implementation:** {action['implementation']}

"""
    
    # Add SHACL profiles if included
    if results.get('shacl_profile_suggestions'):
        report += """## Generated SHACL Profiles

```turtle
"""
        for profile in results['shacl_profile_suggestions']:
            report += profile + "\n\n"
        
        report += "```\n"
    
    report += f"""
---

*Report generated by Universal Document Type Analyzer*  
*CLI Command: `{' '.join(sys.argv)}`*
"""
    
    return report


def main():
    """Main CLI entry point."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate arguments
    validation_errors = validate_arguments(args)
    if validation_errors:
        logger.error("Validation errors:")
        for error in validation_errors:
            logger.error(f"  - {error}")
        sys.exit(1)
    
    try:
        # Run analysis
        results = run_analysis(args)
        
        # Save results
        save_results(results, args)
        
        logger.info("Document type analysis completed successfully!")
        
        # Print summary
        print("\n" + "="*60)
        print("DOCUMENT TYPE ANALYSIS COMPLETE")
        print("="*60)
        print(f"Document Types Found: {len(results['document_types_identified'])}")
        print(f"Total Documents: {results['analysis_metadata']['total_documents_analyzed']}")
        print(f"Output Saved: {args.output}")
        
        if results['document_types_identified']:
            print("\nDocument Types:")
            for doc_type, profile in results['document_types_identified'].items():
                print(f"  - {doc_type}: {len(profile['files'])} files")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Analysis cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())