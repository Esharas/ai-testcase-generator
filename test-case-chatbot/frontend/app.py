import streamlit as st
import requests
import pandas as pd


st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Test Case Generator")

st.write(
    "Enter a requirement and generate detailed software test cases using AI."
)


# --------------------------------------------------
# Requirement input
# --------------------------------------------------

requirement = st.text_area(
    "📝 Requirement",
    placeholder=(
        "Example: User should be able to login "
        "using a valid username and password."
    ),
    height=120
)


# --------------------------------------------------
# Top Action Buttons
# --------------------------------------------------

generate_col, export_col = st.columns([1, 1])


# --------------------------------------------------
# Generate Test Cases
# --------------------------------------------------

with generate_col:

    if st.button(
        "🚀 Generate Test Cases",
        type="primary",
        use_container_width=True
    ):

        if not requirement.strip():

            st.warning(
                "Please enter a requirement."
            )

        else:

            try:

                with st.spinner(
                    "🤖 Generating test cases..."
                ):

                    response = requests.post(
                        "http://127.0.0.1:8000/generate-testcases",
                        json={
                            "requirement": requirement
                        }
                    )


                if response.status_code == 200:

                    result = response.json()

                    # Store test cases
                    st.session_state["test_cases"] = (
                        result["test_cases"]
                    )

                    st.session_state["requirement"] = (
                        requirement
                    )

                    # Remove previously generated Excel
                    if "excel_file" in st.session_state:
                        del st.session_state["excel_file"]

                    st.success(
                        "✅ Test cases generated successfully!"
                    )

                else:

                    st.error(
                        f"Backend error "
                        f"({response.status_code})"
                    )

                    st.code(
                        response.text
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to FastAPI backend. "
                    "Make sure FastAPI is running."
                )


# --------------------------------------------------
# Excel Export Button
# --------------------------------------------------

with export_col:

    if "test_cases" in st.session_state:

        if st.button(
            "📁 Create & Download Excel",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Creating Excel file..."
                ):

                    excel_response = requests.post(
                        "http://127.0.0.1:8000/generate-excel",
                        json={
                            "test_cases": (
                                st.session_state["test_cases"]
                            )
                        }
                    )


                if excel_response.status_code == 200:

                    # Save Excel in session
                    st.session_state[
                        "excel_file"
                    ] = excel_response.content

                    st.success(
                        "✅ Excel file created successfully!"
                    )


                else:

                    st.error(
                        "❌ Excel generation failed."
                    )

                    st.code(
                        excel_response.text
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to FastAPI backend."
                )


        # ------------------------------------------
        # Download button
        # ------------------------------------------

        if "excel_file" in st.session_state:

            st.download_button(
                label="⬇️ Download Test Cases Excel",
                data=st.session_state["excel_file"],
                file_name="Generated_Test_Cases.xlsx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                ),
                use_container_width=True
            )


# --------------------------------------------------
# Display generated test cases
# --------------------------------------------------

if "test_cases" in st.session_state:

    test_cases = st.session_state["test_cases"]

    st.divider()

    st.subheader(
        f"📋 Generated Test Cases ({len(test_cases)})"
    )


    # --------------------------------------------------
    # Display each test case
    # --------------------------------------------------

    for index, test_case in enumerate(test_cases):

        test_case_id = test_case.get(
            "test_case_id",
            f"TC_{index + 1:03d}"
        )

        title = test_case.get(
            "title",
            "Test Case"
        )

        priority = test_case.get(
            "priority",
            ""
        )

        severity = test_case.get(
            "severity",
            ""
        )


        # --------------------------------------------------
        # Expandable test case
        # --------------------------------------------------

        with st.expander(
            f"🧪 {test_case_id} — {title}",
            expanded=(index == 0)
        ):

            # ----------------------------------------------
            # Test Case information
            # ----------------------------------------------

            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.markdown(
                    "**Requirement ID**"
                )

                st.write(
                    test_case.get(
                        "requirement_id",
                        ""
                    )
                )


            with col2:

                st.markdown(
                    "**Priority**"
                )

                st.write(priority)


            with col3:

                st.markdown(
                    "**Severity**"
                )

                st.write(severity)


            with col4:

                st.markdown(
                    "**Test Result**"
                )

                st.write(
                    test_case.get(
                        "test_results",
                        "Not Executed"
                    )
                )


            # ----------------------------------------------
            # Description
            # ----------------------------------------------

            st.markdown(
                "**Description / Preconditions**"
            )

            st.info(
                test_case.get(
                    "description",
                    ""
                )
            )


            # ----------------------------------------------
            # Test Steps Table
            # ----------------------------------------------

            st.markdown(
                "**Test Steps**"
            )


            steps = test_case.get(
                "steps",
                []
            )


            if steps:

                table_data = []


                for step_number, step in enumerate(
                    steps,
                    start=1
                ):

                    table_data.append(
                        {
                            "Step": step_number,
                            "Test Step": step.get(
                                "step",
                                ""
                            ),
                            "Test Data": step.get(
                                "test_data",
                                ""
                            ),
                            "Expected Result": step.get(
                                "expected_result",
                                ""
                            )
                        }
                    )


                df = pd.DataFrame(
                    table_data
                )


                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )


            else:

                st.warning(
                    "No test steps were generated."
                )


            # ----------------------------------------------
            # Additional information
            # ----------------------------------------------

            st.markdown(
                "**Additional Information**"
            )


            info_col1, info_col2, info_col3 = (
                st.columns(3)
            )


            with info_col1:

                st.markdown(
                    "**Defect ID**"
                )

                st.write(
                    test_case.get(
                        "defect_id",
                        ""
                    ) or "—"
                )


            with info_col2:

                st.markdown(
                    "**Assignee**"
                )

                st.write(
                    test_case.get(
                        "assignee",
                        ""
                    ) or "—"
                )


            with info_col3:

                st.markdown(
                    "**Comment**"
                )

                st.write(
                    test_case.get(
                        "comment",
                        ""
                    ) or "—"
                )