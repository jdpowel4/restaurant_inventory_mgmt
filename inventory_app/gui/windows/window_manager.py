from PySide6.QtWidgets import (
    QMdiArea,
    QMdiSubWindow,
    QWidget
)

from inventory_app.app.app_context import AppContext

class WindowManager:
    """
    Manages Windows displayed inside the app's QMdiArea
    """

    def __init__(
        self,
        mdi_area: QMdiArea,
        context: AppContext
    ):
        self.mdi_area = mdi_area
        self.context = context

    def open(
        self,
        widget: QWidget,
        title: str
    ) -> QMdiSubWindow:
        """
        Add a QWidget to the MDI workspace.

        Parameters
        ----------
        widget:
            The domain-specific GUI widget that should be displayed.

        title:
            Text displayed in the MDI child window's title bar.

        Returns
        -------
        QMdiSubWindow
            The MDI wrapper containing the supplied widget.
        """
        subwindow = self.mdi_area.addSubWindow(widget)
        subwindow.setWindowTitle(title)
        subwindow.show()
        return subwindow
