import pandas as pd
from fpdf import FPDF

# Step 1: Load COVID-19 data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print("Error reading file:", e)
        return None

# Step 2: Analyze numeric summary
def analyze_data(df):
    numeric_df = df.select_dtypes(include='number')
    return numeric_df.describe()

# Step 3: Create custom FPDF class
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'COVID-19 Data Summary Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_table(self, summary_df):
        self.set_font("Arial", size=9)
        page_width = self.w - 2 * self.l_margin
        col_width = page_width / (len(summary_df.columns) + 1)

        # Header Row
        self.cell(col_width, 10, "Metric", border=1)
        for col in summary_df.columns:
            self.cell(col_width, 10, str(col), border=1)
        self.ln()

        # Data Rows
        for idx, row in summary_df.iterrows():
            self.cell(col_width, 10, str(idx), border=1)
            for val in row:
                text = str(round(val, 2)) if isinstance(val, (int, float)) else str(val)
                self.cell(col_width, 10, text, border=1)
            self.ln()

# Step 4: Generate FPDF Report
def generate_fpdf_report(df, filename):
    summary = analyze_data(df)
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_table(summary)
    pdf.output(filename)
    print(f"✅ FPDF report saved as: {filename}")

# Step 5: Main function
def main():
    input_file = "covid_data.csv"
    output_file = "covid_fpdf_report.pdf"
    df = load_data(input_file)
    if df is not None:
        generate_fpdf_report(df, output_file)
    else:
        print("❌ Failed to load data")

if __name__ == "__main__":
    main()
