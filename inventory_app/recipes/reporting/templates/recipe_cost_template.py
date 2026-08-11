from inventory_app.recipes.reporting.base.pdf_document import BasePDF
from inventory_app.recipes.reporting.styles.main import Styles_Main
from inventory_app.recipes.dto import RecipeCostReport


class RecipeCostTemplate:

    def __init__(
            self,
            report: RecipeCostReport
    ):
        self.report = report

    def render(
            self,
            pdf: BasePDF
    ):
        
        pdf.section_header("Recipe Information")

        pdf.subsection_header(self.report.recipe_name)
        pdf.med_text(f"Yield: {self.report.yield_qty:.2f} {self.report.yield_unit}")
        pdf.med_text(f"Serving Size: {self.report.serving_qty:.2f} {self.report.serving_unit}")
        pdf.med_text(f"# of Servings: {self.report.num_of_servings}")
        
        pdf.ln(.5)


        pdf.section_header("Ingredients")
        
        pdf.recipe_table(self.report.component_lines)
        pdf.section_header("Summary")
        pdf.subsection_header(f"Total Cost: {pdf.money(self.report.total_cost)}")
        pdf.subsection_header(f"Cost per Yield Unit: {pdf.money(self.report.cost_per_yield_unit)}")
        pdf.subsection_header(f"Cost per Serving: {pdf.money(self.report.cost_per_serving)}")