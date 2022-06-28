from PyQt6.QtWidgets import QApplication,QMainWindow, QMessageBox
from movies import *
from actors import *
from homework import *
from casting import *
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connection = db_connection()
        self.loadToCastingTable(selectFromTableAll(self.connection, "casting"))
        self.actors = selectFromTableAll(self.connection, "actors")
        self.films = self.selectFromTable(self.connection, "movies")
        self.loadFilmsToTable(self.films)
        self.loadToActorsTable(self.actors)
        self.ui.lactorsearch.textChanged.connect(self.searchActor)
        self.ui.btnaddactor.clicked.connect(self.addActor)
        self.ui.lfilmsearch.textChanged.connect(self.searchfilm)
        self.ui.btnfilmadd.clicked.connect(self.addFilm)
        self.ui.btncastingadd.clicked.connect(self.addCasting)
        self.ui.btncastingdelete.clicked.connect(self.deleteCasting)
        self.laodAllCastings(self.showAllCasting())
        self.ui.lallsearch.textChanged.connect(self.searchAllCasting)
        self.ui.btn4shart.clicked.connect(self.shart4)
        self.ui.btn4reset.clicked.connect(self.reset)
        self.ui.btndelete.clicked.connect(self.bigdelete)
    #  btn big delete

    def delWarning(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Are you sure you want to delete this info!!!")
        msg.setWindowTitle("Warning!!!")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        res = msg.exec()
        return res == QMessageBox.StandardButton.Yes

    def bigdelete(self):
        id = self.ui.ldelete.text()
        if id.isdigit() and self.delWarning():
            if self.ui.rbdelact.isChecked():
                bigDelete(self.connection, "actors", id, "act_id")
                bigDelete(self.connection, "casting", id, "actor_id")
            elif self.ui.rbdelfilm.isChecked():
                bigDelete(self.connection, "movies", id, "ID")
                bigDelete(self.connection, "casting", id, "film_id")
            self.ui.ldelete.setText("")
            self.loadToCastingTable(self.selectFromTable(self.connection, "casting"))
            self.laodAllCastings(self.showAllCasting())
            self.loadToActorsTable(self.selectFromTable(self.connection, "actors"))
            self.loadFilmsToTable(self.selectFromTable(self.connection, "movies"))
        else:
            self.ui.ldelete.setText("")
    # all is displayed
    def reset(self):
        self.laodAllCastings(self.showAllCasting())
        self.ui.lallsearch.setText("")

    def showAllCasting(self):
        try:
            castings = selectAllFromCasting(self.connection)
            print(castings)
            return castings
        except Exception as ex:
            print(ex)

    def laodAllCastings(self, castings):
        row = 0
        self.ui.casting_jurnal.setRowCount(len(castings))
        for casting in castings:
            self.ui.casting_jurnal.setItem(row, 0, QtWidgets.QTableWidgetItem(casting["act_fname"]))
            self.ui.casting_jurnal.setItem(row, 1, QtWidgets.QTableWidgetItem(casting["act_lname"]))
            self.ui.casting_jurnal.setItem(row, 2, QtWidgets.QTableWidgetItem(casting["mov_title"]))
            self.ui.casting_jurnal.setItem(row, 3, QtWidgets.QTableWidgetItem(casting["role"]))
            self.ui.casting_jurnal.setItem(row, 4, QtWidgets.QTableWidgetItem(casting["mov_lang"]))
            self.ui.casting_jurnal.setItem(row, 5, QtWidgets.QTableWidgetItem(str(casting["mov_year"])))
            row += 1

    def searchAllCasting(self):
        castings = selectAllFromCasting(self.connection)
        text = self.ui.lallsearch.text()
        if text != "":
            if self.ui.rballact.isChecked():
                res = list(filter(lambda x: x["act_fname"].lower().startswith(text.lower()) or \
                    x["act_lname"].lower().startswith(text.lower()), castings))
            else:
                res = list(filter(lambda x: x["mov_title"].lower().startswith(text.lower()), castings))
            self.laodAllCastings(res)
        else:
            self.laodAllCastings(self.showAllCasting())

    def shart4(self):
        castings = selectAllFromCasting(self.connection)
        res = list(filter(lambda x: (x["mov_lang"] == "Uzbek") and (x["mov_year"] > 1995 and x["mov_year"] < 2015), castings))
        self.laodAllCastings(res)


    # casting
    def addCasting(self):
        actor_id = self.ui.lcasting_actor_id.text()
        film_id = self.ui.lcasting_filmID.text()
        role = self.ui.lcastingRole.text()
        films = self.selectFromTable(self.connection, "movies")
        actors = self.selectFromTable(self.connection,  "actors")
        if actor_id.isdigit() and film_id.isdigit() and role != "":
            if int(actor_id) <= actors[-1]["act_id"] and int(actor_id) >= 0 \
                    and int(film_id) <= films[-1]["ID"] and int(film_id) >= 0:
                insertIntoCasting(self.connection, actor_id, film_id, role.title())
        self.loadToCastingTable(selectFromTableAll(self.connection, "casting"))
        self.ui.lcastingRole.setText("")
        self.ui.lcasting_actor_id.setText("")
        self.ui.lcasting_filmID.setText("")
        self.laodAllCastings(self.showAllCasting())

    def deleteCasting(self):
        actor_id = self.ui.lcasting_actor_id.text()
        film_id = self.ui.lcasting_filmID.text()
        if film_id.isdigit() and actor_id.isdigit():
            deleteFromCasting(self.connection,actor_id,film_id)
            self.loadToCastingTable(self.selectFromTable(self.connection, "casting"))
            self.ui.lcastingRole.setText("")
            self.ui.lcasting_actor_id.setText("")
            self.ui.lcasting_filmID.setText("")

    def loadToCastingTable(self, casts):
        self.ui.castingtable.setRowCount(len(casts))
        row = 0
        for cast in casts:
            self.ui.castingtable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(cast["actor_id"])))
            self.ui.castingtable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(cast["film_id"])))
            self.ui.castingtable.setItem(row, 2, QtWidgets.QTableWidgetItem(cast["role"]))
            row += 1



    # Films
    def loadFilmsToTable(self, films):
        self.ui.filmtable.setRowCount(len(films))
        row = 0
        for film in films:
            self.ui.filmtable.setItem(row, 0,QtWidgets.QTableWidgetItem(str(film["ID"])))
            self.ui.filmtable.setItem(row, 1,QtWidgets.QTableWidgetItem(film["mov_title"]))
            self.ui.filmtable.setItem(row, 2,QtWidgets.QTableWidgetItem(str(film["mov_year"])))
            self.ui.filmtable.setItem(row, 3,QtWidgets.QTableWidgetItem(str(film["mov_time"])))
            self.ui.filmtable.setItem(row, 4,QtWidgets.QTableWidgetItem(film["mov_lang"]))
            row += 1

    def searchfilm(self):
        try:
            with self.connection.cursor() as cursor:
                text = self.ui.lfilmsearch.text()
                if self.ui.rbname.isChecked():
                    sql = f"SELECT * FROM movies where mov_title like '{text}%'"
                elif self.ui.rbyear.isChecked():
                    sql = f"SELECT * FROM movies where mov_year like '{text}%'"
                elif self.ui.rblanguage.isChecked():
                    sql = f"SELECT * FROM movies where mov_lang like '{text}%'"
                cursor.execute(sql)
                films = cursor.fetchall()
            if text != "":
                self.loadFilmsToTable(films)
            else:
                self.loadFilmsToTable(self.films)

        except Exception as ex:
            print(ex)

    def addFilm(self):
        try:
            name = self.ui.lfilmname.text()
            year = self.ui.lfilmyear.text()
            time_f = self.ui.lfilmtime.text()
            language = self.ui.lfilmlang.text()
            if name != "" and year.isdigit() and self.isrightime(time_f) and language != "":
                insertIntoTablefilms(self.connection, name.title(),year, time_f, language.title())
            self.loadFilmsToTable(selectFromTableAll(self.connection,"movies"))
            self.ui.lfilmlang.setText("")
            self.ui.lfilmtime.setText("")
            self.ui.lfilmname.setText("")
            self.ui.lfilmyear.setText("")
        except Exception as ex:
            print(ex)


    @staticmethod
    def isrightime(time_f:str):
        time_f = time_f.split(":")
        if len(time_f) in [3, 2]:
            for j in time_f:
                if not j.isdigit():
                    return False
            else:
                return True
        else:
            return False

    # actors
    @staticmethod
    def selectFromTable(connection, table):
        return selectFromTableAll(connection, f"{table}")

    def addActor(self):
        fname = self.ui.lactorfname.text()
        lname = self.ui.lactorlname.text()
        gender = self.ui.lactorgender.text()
        if fname != "" and lname != "" and gender != "":
            insertToTableActors(self.connection, fname.title(),lname.title(),gender.lower())
            actors = selectFromTableAll(self.connection, "actors")
            self.loadToActorsTable(actors)
            self.ui.lactorfname.setText("")
            self.ui.lactorlname.setText("")
            self.ui.lactorgender.setText("")

    def searchActor(self):
        try:
            with self.connection.cursor() as cursor:
                text = self.ui.lactorsearch.text()
                if self.ui.rbboth.isChecked():
                    sql = f"Select * from actors where act_fname like '{text}%' or " \
                          f"act_lname like '{text}%'"
                elif self.ui.rbmale.isChecked():
                    sql = f"Select * from actors where (act_fname like '{text}%' or " \
                          f"act_lname like '{text}%') and " \
                          f"act_gender = 'm'"
                else:
                    sql = f"Select * from actors where" \
                          f" (act_fname like '{text}%' or " \
                          f"act_lname like '{text}%') and " \
                          f"act_gender = 'f'"
                cursor.execute(sql)
                actors = cursor.fetchall()
                if text != "":
                    self.loadToActorsTable(actors)
                else:
                    self.loadToActorsTable(self.actors)
        except Exception as ex:
            print(ex)


    def loadToActorsTable(self, actors):
        self.ui.actortable.setRowCount(len(actors))
        row = 0
        for actor in actors:
            self.ui.actortable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(actor["act_id"])))
            self.ui.actortable.setItem(row, 1, QtWidgets.QTableWidgetItem(actor["act_fname"]))
            self.ui.actortable.setItem(row, 2, QtWidgets.QTableWidgetItem(actor["act_lname"]))
            self.ui.actortable.setItem(row, 3, QtWidgets.QTableWidgetItem(actor["act_gender"]))
            row += 1


def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()