from inventory_app.recipes.reporting.base.pdf_document import BasePDF
from inventory_app.recipes.reporting.templates.recipe_cost_template import RecipeCostTemplate
from inventory_app.recipes.dto import ReportMetadata
from inventory_app.business.providers.business_provider import BusinessProvider

class PDFExporter:

    def export(
            self,
            template: RecipeCostTemplate,
            metadata: ReportMetadata,
    ):
        pdf = BasePDF()

        pdf.set_title(metadata.title)
        pdf.set_author(metadata.author)
        pdf.set_subject(metadata.subject)
        pdf.set_creation_date(metadata.created)

        pdf.add_page()
        pdf.page_title(metadata.title)

        template.render(pdf)

        pdf.output(metadata.filename)