# -*- coding: utf-8 -*-

import webbrowser

from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex, pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, \
    QAbstractItemView, QHBoxLayout


# =========================================================
#
# =========================================================


def parent_load_json(parent, d):
    if isinstance(d, dict):
        for key, value in d.items():
            it = QStandardItem(str(key))
            if isinstance(value, dict):
                parent.appendRow(it)
                parent_load_json(it, value)
            else:
                it2 = QStandardItem(str(value))
                parent.appendRow([it, it2])


# https://stackoverflow.com/questions/70934947/qt-and-python-qidentityproxymodel-does-not-get-the-right-column-count-when-nes
# https://stackoverflow.com/questions/70934947/qt-and-python-qidentityproxymodel-does-not-get-the-right-column-count-when-nes


# ===========================================================


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDynamicSortFilter(True)

        self.setRecursiveFilteringEnabled(True)  # !!!!!
        self.searchText = None

    def setSearchText(self, arg=None):
        self.searchText = arg
        self.invalidateFilter()  # !!!!!  reset

    def filterAcceptsRow(self, sourceRow, sourceParent) -> bool:
        if self.searchText is None:
            return True  # gut
        # проверим, что моделька валидная
        model = self.sourceModel()
        if model is None:
            return False

        # print(self.filterKeyColumn(),)

        index = model.index(sourceRow, self.filterKeyColumn(), sourceParent)
        if not index.isValid():
            return False  # !!!!! False False False
        item = model.itemFromIndex(index)  # .internalPointer()
        current = item.text()
        if self.searchText in current:
            return True
        return False


# =========================================================
#
# =========================================================
#     # proxyModel.invalidateColumnsFilter()
#     # proxyModel.invalidateFilter()
#     proxyModel.setFilterKeyColumn(1)
#     # sourceModel.dataChanged.emit(ind,ind)
#     view.setSortingEnabled(True)
"""
        # https://stackoverflow.com/questions/51199230/how-to-add-column-before-treecolumn-in-qt-qtreeview
        # self.header().swapSections(2, 1);
        # self.header().swapSections(0, 1);
        self.header().moveSection(2, 0);
        self.setTreePosition(0)

"""


class MainFrame(QDialog):
    def __init__(self, parent, tree_data):
        super(MainFrame, self).__init__(parent)

        self.sourceModel = QStandardItemModel()
        self.sourceModel.setHorizontalHeaderLabels(["Level", "Values"])

        parentItem = self.sourceModel.invisibleRootItem()
        parent_load_json(parentItem, tree_data)

        self.proxyModel = CustomSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.sourceModel)
        # self.proxyModel.setFilterKeyColumn(1)

        self.w_tree = QTreeView()
        self.w_tree.setModel(self.proxyModel)
        self.w_tree.doubleClicked.connect(self.act_doubleClicked)

        self.w_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.w_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.w_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.w_tree.setColumnWidth(0, 500)

        self.w_tree.setSortingEnabled(True)
        self.w_tree.sortByColumn(1, Qt.AscendingOrder);



        #
        self.w_filterEdit = QLineEdit()
        self.w_filterEdit.textChanged.connect(self.act_w_filterEdit)
        #
        self.w_checkb = QCheckBox("Filter by column 1 (otherwise 0)")
        self.w_checkb.toggled.connect(lambda: self.btnstate(self.w_checkb))

        #
        self.button = QPushButton("append in tree")
        self.button.clicked.connect(self.act_bt_append)

        self.bt_sort = QPushButton("clear sort")
        self.bt_sort.clicked.connect(self.act_bt_sort)

        self.bt_pos = QPushButton("tree pos")
        self.bt_pos.clicked.connect(self.act_bt_pos)

        self.bt_moveSection = QPushButton("moveSection")
        self.bt_moveSection.clicked.connect(self.act_bt_moveSection)

        layout = QVBoxLayout(self)
        layout.addWidget(self.w_filterEdit)
        layout.addWidget(self.w_checkb)
        layout.addWidget(self.w_tree)
        bt = QHBoxLayout(self)
        for w in [self.button, self.bt_sort, self.bt_pos, self.bt_moveSection]:
            bt.addWidget(w)

        layout.addLayout(bt)
        #
        self.w_tree.expandAll()
        self.setMinimumSize(640, 480)

    def get_current_parent(self, curr_ind=None):
        if curr_ind is None:
            try:
                curr_ind = self.w_tree.selectedIndexes()[0]
            except:
                curr_ind = QModelIndex()

        if curr_ind.isValid():
            model = self.w_tree.model()
            if isinstance(model, QSortFilterProxyModel):  # convert
                curr_ind = source_index = model.mapToSource(curr_ind)
            parent = self.sourceModel.itemFromIndex(curr_ind)

        else:
            parent = self.sourceModel.invisibleRootItem()

        return parent

    def act_w_filterEdit(self, text):
        self.proxyModel.setSearchText(text)
        self.w_tree.expandAll()

    def act_bt_append(self):
        __ = {"Root 1": {}}
        parent_load_json(self.get_current_parent(), __)
        self.w_tree.expandAll()

    def act_bt_sort(self):
        # https://www.linux.org.ru/forum/development/12578241
        self.proxyModel.sort(-1)
        # self.w_tree.sortByColumn(-1, Qt.AscendingOrder);

    def act_bt_pos(self):
        pos = 0 if self.w_tree.treePosition() else 1
        self.w_tree.setTreePosition(pos)

    def act_bt_moveSection(self):
        # https://stackoverflow.com/questions/51199230/how-to-add-column-before-treecolumn-in-qt-qtreeview
        self.w_tree.header().moveSection(1, 0);

    def btnstate(self, b):
        column = 1 if b.isChecked() else 0
        self.proxyModel.setFilterKeyColumn(column)

    @pyqtSlot(QModelIndex)
    def act_doubleClicked(self, index: QModelIndex) -> None:
        if index.isValid() and index.column() == 1:
            try:
                txt = self.get_current_parent(index).text()
                if txt:
                    webbrowser.open_new_tab(txt)
            except Exception as err:
                print(err)


# =========================================================
#
# =========================================================

d_QAbstractProxyModel = {"QIdentityProxyModel": '',
       "QSortFilterProxyModel": 'https://doc.qt.io/qt-5/qsortfilterproxymodel.html',
       "QTransposeProxyModel": ''
                         }
# -----------------------
d_qtreeview = {'QTreeView':
           {'QTreeView->header().moveSection': ' !!!!!!',
            'QTreeView->header().swapSections(0, 1)':
                'https://stackoverflow.com/questions/51199230/how-to-add-column-before-treecolumn-in-qt-qtreeview',

            'QTreeView->setColumnWidth': ' !!!!!!!',
            'QTreeWidget': 'https://doc.qt.io/qt-5/qtreewidget.html'

            }

               }
# --------------------------
dict_tree = {
    "QObject": {
        "QAbstractItemModel": {
            "QAbstractProxyModel": d_QAbstractProxyModel,
            "QAbstractListModel":
                {'QStringListModel': 'https://doc.qt.io/qt-5/qstringlistmodel.html'},

            "QAbstractTableModel": '',
            "QConcatenateTablesProxyModel": '',
            "QDirModel": 'https://doc.qt.io/qt-5/qdirmodel.html',
            "QFileSystemModel": '',
            "QStandardItemModel": ''

        },
        "QAbstractItemDelegate": {
            "QItemDelegate": 'https://doc.qt.io/qt-5/qitemdelegate.html',
            "QStyledItemDelegate": {
                "url": 'https://doc.qt.io/qt-5/qstyleditemdelegate.html',
                "txt": 'The QStyledItemDelegate class provides display and editing facilities for data items from a model',

            },
        },

        "enum SortOrder": ' { AscendingOrder, DescendingOrder }',
        "Отмена сортировки через прокси-модель": 'https://www.linux.org.ru/forum/development/12578241',
        "QAbstractItemView": d_qtreeview,
    }
}
# =========================================================
#                       __main__
# =========================================================
if __name__ == "__main__":
    app = QApplication([])
    main = MainFrame(None, dict_tree)
    main.show()
    app.exec_()
