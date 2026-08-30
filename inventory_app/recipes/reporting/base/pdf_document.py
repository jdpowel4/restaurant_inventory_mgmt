from fpdf import FPDF
from datetime import date, datetime
from typing import List

from inventory_app.shared.db import session_scope
from inventory_app.shared.config import ASSET_DIR
from inventory_app.business.providers.business_provider import BusinessProvider
from inventory_app.business.services.business_service import BusinessService
from inventory_app.recipes.reporting.styles.main import Styles_Main
from inventory_app.recipes.dto import ComponentCostLine

class BasePDF(FPDF):
    """
    General PDF Layout for all PDF Documents. Includes Letter Head, Footer, Section Header, Money Formats, and Quantity Formats
    """

    def __init__(
        self,
    ):
        super().__init__(
            orientation="p",
            unit="in",
            format="letter"
        )

        with session_scope() as session:
            
            provider = BusinessProvider()
            provider.load(session)

            self._business = provider.business
            self.logo_path = ASSET_DIR / self._business.logo_path
            
            

        self.set_auto_page_break(True, margin=0.5)
        self.set_top_margin(Styles_Main.TOP_MARGIN)
        self.set_left_margin(Styles_Main.LEFT_MARGIN)
        self.set_right_margin(Styles_Main.RIGHT_MARGIN)

    def header(self):
        """
        General Letter Head for all Documents.
        Includes Title, Logo, and Business Info
        """

        self.set_y(.25)
        self.set_line_width(.0075)
        self.set_draw_color(15,15,15)
        self.line(.5, .25, 8, .25)
        self.ln(.05)
        self.line(.5, .3, 8, .3)
        self.image(self.logo_path, .25, .15, 1.25)
        self.set_y(.475)
        self.set_font(*Styles_Main.TITLE_FONT)
        self.set_x(1.35)
        self.cell(0, .3, self._business.name, new_x="LMARGIN", new_y="NEXT")
        self.set_x(1.35)
        self.set_font(*Styles_Main.MEDIUM_FONT)
        self.cell(0, .18, self._business.address, new_x="LMARGIN", new_y="NEXT")
        self.set_x(1.35)
        self.cell(0, .18, self._business.phone)
        self.set_xy(6.85, .35)
        self.cell(0, .18, f"Date: {date.today()}", align="L",new_x="LEFT", new_y="NEXT")
        self.cell(0, .18, f"Time: {datetime.now().time().strftime("%I:%M %p")}", align="L")
        self.line(0.5, 1.35, 8, 1.35)
        
    
    def footer(self):
        """
        General Footer for all Documents.
        Includes Page Numbers
        """
        self.set_y(-1)
        self.set_font(*Styles_Main.MEDIUM_FONT)
        self.cell(0, 1, f"Page {self.page_no()}", align="C")

    def page_title(self, text):
        
        self.set_y(1.5)
        self.set_font(*Styles_Main.TITLE_FONT)
        self.cell(None, .3, text, "B", center=True)
        
        self.ln(.5)

    def section_header(self, text):
        """
        """
        self.set_font(*Styles_Main.SECTION_FONT)
        self.set_fill_color(*Styles_Main.HEADER_FILL)
        self.cell(None, 0.25, text, "B", fill=True)
        self.ln(.35)
    
    def subsection_header(self, text):

        self.set_font(*Styles_Main.SUBSECTION_FONT)
        self.cell(None, 0.25, text)
        self.ln(.25)

    def large_bold_text(self, text):

        self.set_font(*Styles_Main.LARGE_BOLD_FONT)
        self.cell(None, 0.25, text)

    def med_text(self, text):

        self.set_font(*Styles_Main.MEDIUM_FONT)
        self.cell(None, 0.25, text)
        self.ln(.15)

    def body(self):
        
        self.set_font(*Styles_Main.MEDIUM_FONT)

    def recipe_table(self, component_lines: List[ComponentCostLine]):

        headers = [
            "Ingredient",
            "Quantity",
            "Unit Cost",
            "Extended Cost"
        ]

        widths = [3.25, 1.25, 1.25, 1.25]

        # Header
        self.set_font(*Styles_Main.TABLE_HEADER_FONT)
           
        for h, w in zip(headers, widths):
            self.cell(w, .25, h, border=1, fill=True)
        self.ln()
        # Body
        
        for line in component_lines:

            self.set_font(*Styles_Main.MEDIUM_FONT)

            self.cell(widths[0], .25, line.component_name, border=1)
            self.cell(widths[1], .25, self.qty(line.recipe_quantity, line.recipe_unit), border=1)
            self.cell(widths[2], .25, f"{self.money(line.recipe_unit_cost)}/{line.recipe_unit}", border=1, align="R")

            self.set_font(*Styles_Main.MONEY_FONT)

            self.cell(widths[3], .25, self.money(line.total_cost), border=1, align="R")
               
            self.ln()

        self.set_font(*Styles_Main.MEDIUM_FONT)

        self.ln()
            

    def money(self, amount):
        """
        """
        return f"${amount:,.2f}"

    def qty(self, qty, unit):
        """
        """
        return f"{qty:.2f} {unit}"
    