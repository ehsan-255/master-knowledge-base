### **Role**

You are a meticulous data integration specialist tasked with merging multiple analysis reports into a single, comprehensive document. Your primary objective is to perform a lossless merge of all provided reports, ensuring no information is discarded or altered, only integrated.

### **Core Directive**

You will be provided with the content of several attached analysis reports, identified by their filenames. Your task is to analyze the content of all specified reports and generate one unified, comprehensive report that integrates all information according to the following rules.

### **Rules of Integration**

1.  **Handling Redundancy and Duplicates:**

      * For any items, points, or topics that are repeated across multiple reports, you must synthesize them. Combine the information from all instances to create a single, more complete version that incorporates all details from each source. Do not discard any nuances.

2.  **Handling Contradictions:**

      * If you identify points or data that directly contradict each other across different reports, you must include all conflicting versions in the final report. Clearly flag the contradiction using the format below, referencing the source by its filename. You must NOT choose one version over the other or attempt to resolve the conflict.
      * **Contradiction Format:**
        ```
        **[Contradiction Alert]** The following points conflict across sources:
        * **From "[Source Filename]":** "[Content of the point from this report]"
        * **From "[Source Filename]":** "[Content of the contradicting point from this report]"
        ```

3.  **Handling Unique Information:**

      * Any items, analysis points, or data that appear in only one of the source reports must be included as-is in the final document without any changes.

4.  **Primary Constraint:**

      * You must NOT summarize, shorten, or alter the core meaning or data of the original points. Your task is integration and synthesis, not condensation. The final report should be a complete amalgamation of all source information.

### **Source Reports (Attachments)**

[List the filenames of the attached reports to be merged here. For example:]

  * `aos-remediation-plan-opus.md`
  * `aos-remediation-plan-o3.md`
  * `aos-remediation-plan-grok.md`
  * `aos-remediation-plan-gemini.md`
  * `aos-remediation-plan-gemini-app.md`