# standartine GUI biblioteka
import threading
import time
import tkinter.tix as tkx
from functools import partial

# Reikalingos parsisiusti bibliotekos
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


# Naudotas saltinis diagramoms braizyti
## https://datatofish.com/matplotlib-charts-tkinter-gui/


class Constants:
    # Konstantu klase

    # Langu pavadinimu konstantos, skirtos pakeisti rodoma langa vartotojui
    WINDOW_HOME = "WINDOW_HOME"
    WINDOW_GRAPHIC = "WINDOW_GRAPHIC"

    # Langu pavadinimai
    TITLE_HOME = "Donatas Žitkus, v0.00001 beta"
    TITLE_GRAPHIC = "Donatas Žitkus, v0.00001 beta"

    # Minimalus lango dydis
    MIN_WIDTH = 640
    MIN_HEIGHT = 480


class DiagramData:
    # Klase skirta laikyti diagramos duomenis
    # X ir Y asiu pavadinimai
    # X asies duomenys, Y asies duomenys (vykdymo laiko atvaizdavimas)
    def __init__(self, xtitle, xdata, ytitle, ydata):
        self.xtitle = xtitle
        self.xdata = xdata
        self.ytitle = ytitle
        self.ydata = ydata

    def getDiagramAsDictionary(self):
        "Metodas skirtas diagramos duomenis atvaizduoti kaip dictionary"
        return {self.xtitle: self.xdata, self.ytitle: self.ydata}


class WindowUtils:
    def clearWindow(window):
        "Metodas skirtas pasalinti visus lange esancius elementus (widgets)"
        for widget in window.winfo_children():
            widget.destroy()
        window.pack_forget()
        window.grid_forget()


class Actions:
    # Funkciju vykdymo laikas skirtingais metodais
    workTimeOnThread = 0  # Vykdymas Threadais
    workTimeNormal = 0  # Nuoseklus vykdymas

    def _generateRandomArray(self, amount):
        # Sugeneruojamas atsitiktinis masyvas pagal vartotojo nurodyta kieki, reiksmes nuo 1 iki 1000
        self._numberArray = np.random.randint(low=1, high=1000, size=amount)

    def _calculateSumOfArray(self, array):
        "Metodas skirtas masyvo nariu sumai apskaiciuoti"
        sum = 0
        for el in array:
            sum += el
        return sum

    def _multiplyArray(self, array):
        "Metodas skirtas masyvo nariu sandaugai apskaiciuoti"
        multi = 1
        for el in array:
            multi = multi * el
        return multi

    def _min(self, array):
        "Metodas skirtas maziausia masyvo nari rasti"
        min = array[0]
        for i in range(1, len(array)):
            if array[i] < min:
                min = array[i]
        return min

    def doActionsNormally(self, arraySize):
        "Metodas skirtas uzduotis ivykdyti nuosekliai"
        startTime = time.perf_counter()
        self._generateRandomArray(amount=arraySize)
        sum = self._calculateSumOfArray(self._numberArray)
        multi = self._multiplyArray(self._numberArray)
        min = self._min(self._numberArray)
        self.workTimeNormal = time.perf_counter() - startTime

    def _doActionsOnTwoThreads1(self, arraySize):
        self._generateRandomArray(amount=arraySize)
        sum = self._calculateSumOfArray(self._numberArray)

    def _doActionsOnTwoThreads2(self):
        multi = self._multiplyArray(self._numberArray)
        min = self._min(self._numberArray)

    def _doActionsOnThreeThreads1(self, arraySize):
        self._generateRandomArray(amount=arraySize)

    def _doActionsOnThreeThreads2(self):
        sum = self._calculateSumOfArray(self._numberArray)
        multi = self._multiplyArray(self._numberArray)

    def _doActionsOnThreeThreads3(self):
        min = self._min(self._numberArray)

    def doActionsOnThreads(self, arraySize, numberOfThreads):
        # Vartotojas nurode, jog veiksmai bus vykdomi viename Thread'e
        if numberOfThreads == 1:
            # laikas pries funkcijos vykdyma
            startTime = time.perf_counter()
            # sukuriamas naujas threadas
            thr = threading.Thread(target=self.doActionsNormally, args=(arraySize,))
            thr.start()
            # palaukiama, kol thread'as ivykdys veiksmus
            thr.join()
            # apskaiciuojamas vykdymo laikas
            self.workTimeOnThread = time.perf_counter() - startTime
        elif numberOfThreads == 2:
            listOfThreads = []
            thr1 = threading.Thread(target=self._doActionsOnTwoThreads1, args=(arraySize,))
            listOfThreads.append(thr1)
            thr2 = threading.Thread(target=self._doActionsOnTwoThreads2)
            listOfThreads.append(thr2)
            startTime = time.perf_counter()
            thr1.start()
            thr2.start()
            for t in listOfThreads:
                t.join()
            self.workTimeOnThread = time.perf_counter() - startTime
        elif numberOfThreads == 3:
            listOfThreads = []
            thr1 = threading.Thread(target=self._doActionsOnThreeThreads1, args=(arraySize,))
            listOfThreads.append(thr1)
            thr2 = threading.Thread(target=self._doActionsOnThreeThreads2)
            listOfThreads.append(thr2)
            thr3 = threading.Thread(target=self._doActionsOnThreeThreads3)
            listOfThreads.append(thr3)

            startTime = time.perf_counter()
            thr1.start()
            thr2.start()
            thr3.start()

            for t in listOfThreads:
                t.join()
            self.workTimeOnThread = time.perf_counter() - startTime


# Metodas paveldi informacija is klases Frame ir WindowUtils
class Home(tkx.Frame, WindowUtils):
    def __init__(self, parent, controller):
        tkx.Frame.__init__(self, parent)
        self._controller = controller

        self._actions = Actions()

    def entryChangeListener(self, *args):
        "Metodas skirtas stebeti vartotojo koreguojamus elementus ir pagal tai leisti/neleisti veiksmu vykdyma"
        if (len(self._numberValue.get()) > 0 and len(self._threadValue.get())) > 0 or (
                len(self._numberValue.get()) > 0 and self._optionsMenuValue[1] == 0):
            self._submitButton.config(state='normal')
        else:
            self._submitButton.config(state='disabled')

    def refresh(self, bundle):
        # Nustatomas lango pavadinimas
        self._controller.title(Constants.TITLE_HOME)
        # Isvalomi pries tai lange buve elementai pasinaudojant elementu is klases WindowUtils (paveldejimas)
        self.clearWindow()

        infoLabel = tkx.Label(self,
                              text="Iveskite didesni uz 0 sveika skaiciu \nis kurio bus sugeneruotas jusu nurodyto dydzio teigiamu skaiciu masyvas")
        infoLabel.pack()

        self._numberValue = tkx.StringVar(self)
        self._numberValue.trace("w", self.entryChangeListener)

        self._threadValue = tkx.StringVar(self)
        self._threadValue.trace("w", self.entryChangeListener)

        self._numberEntry = tkx.Entry(self, textvariable=self._numberValue)
        self._numberEntry.pack()

        threadInfoLabel = tkx.Label(self,
                                    text="Iveskite sveika skaiciu, kuris nurodys pasirinktu giju kieki (maziausiai 1, daugiausiai 3)")
        threadInfoLabel.pack()

        self._threadsEntry = tkx.Entry(self, textvariable=self._threadValue)
        self._threadsEntry.pack()

        typeInfoLabel = tkx.Label(self,
                                  text="Pasirinkite programos veiksmu vykdymo budus")
        typeInfoLabel.pack()

        self._choicesFrame = tkx.Frame(self)
        self._choicesFrame.pack()

        # CheckBoxes arba kitaip veiksmu vykdymo tipu pasarinkimas
        self._choices = ("Nuoseklus vykdymas", "Gijomis paremtas vykdymas")
        self._optionsMenuValue = []
        self._optionsMenuButtons = []
        for i in range(len(self._choices)):
            # Nustatoma mygtuko reiksme. 1 - pasirinkta, 0 - nepasirinkta
            self._optionsMenuValue.append(tkx.IntVar(value=1))
            self._optionsMenuValue[i].trace("w", self.entryChangeListener)
            self._optionsMenuButtons.append(
                tkx.Checkbutton(self._choicesFrame, text=self._choices[i], variable=self._optionsMenuValue[i],
                                onvalue=1, offvalue=0))
            self._optionsMenuButtons[i].pack()

        self._buttonsFrame = tkx.Frame(self)
        self._buttonsFrame.pack()

        self._submitButton = tkx.Button(self._buttonsFrame, text="Vykdyti")
        self._submitButton.pack(side="left", anchor=tkx.NW, expand=True, )
        # Veiksmu vykdyma perkeliu i atskira Thread'a, kad neatsitiktu taip, jog esant dideliam duomenu kiekiui
        # programa taps "not responding"
        self._submitButton.config(command=lambda: threading.Thread(target=self.doActions).start(), state='disabled')

        self._clearButton = tkx.Button(self._buttonsFrame, text="Isvalyti")
        self._clearButton.pack(side="left", anchor=tkx.NW, expand=True, )
        self._clearButton.config(command=partial(self._actionClear))

        self._exitButton = tkx.Button(self._buttonsFrame, text="Uzdaryti")
        self._exitButton.pack(side="left", anchor=tkx.NW, expand=True, )
        self._exitButton.config(command=lambda: self._controller.exit())

        self._errorLabel = tkx.Label(self, text="")
        self._errorLabel.pack()

        self._progressLabel = tkx.Label(self, text="")
        self._progressLabel.pack()

    def _actionClear(self):
        "Metodas skirtas isvalyti vartotojo pasirinkimus CheckBox'uose"
        if len(self._numberValue.get()) > 0 or len(self._threadValue.get()) > 0 or self.checkboxesAreModified():
            self._numberValue.set("")
            self._threadValue.set("")
            for i in range(len(self._optionsMenuValue)):
                self._optionsMenuValue[i].set(value=1)

    def checkboxesAreModified(self):
        "Metodas skirtas patikrinti, ar vartotojas atliko pakeitimus "
        for c in self._optionsMenuValue:
            if c.get() == 0:
                return True
        return False

    def allChecboxesUnselected(self):
        "Metodas skirtas patikrinti, ar visi Checkbox'ai nera pazymeti"
        for c in self._optionsMenuValue:
            if c.get() == 1:
                return False
        return True

    def checkErrors(self):
        errorText = ""
        errors = False

        try:
            nValue = int(self._numberValue.get())
            # Vartotojo ivesta reiksme turi buti nurodytame intervale
            if nValue < 1 or nValue > 9999999:
                raise Exception
        except Exception:
            errorText += "* Pirmame laukelyje nurodytas skaicius turi buti sveikas ir didesnis uz 0 ir mazesnis uz 9999999"
            errors = True
        try:
            tValue = int(self._threadValue.get())
            # Vartotojo nurodytas Thread'u skaicius turi buti siame intervale
            if tValue < 1 or tValue > 3:
                raise Exception
        except Exception:
            errorText += "\n* Antrame laukelyje blogai nurodytas giju skaicius"
            errors = True
        if self.allChecboxesUnselected():
            errorText += "\n* Pasirinkite bent viena atlikimo buda"
            errors = True

        # Grazinamas error tekstas ir boolean tipo reiksme errors, kuri parodo, ar bent vienas neatitikimas buvo rastas
        return errorText, errors

    def doActions(self):
        "Metodas skirtas vykdyti uzduotyje nurodytus veiksmus"
        self._progressLabel.config(text="Vykdoma. Prasau palaukti")
        errorText, hasErrors = self.checkErrors()

        xdata = []
        ydata = []

        # Bent viena klaida buvo rasta
        if hasErrors:
            self._errorLabel.config(text=errorText)
        else:
            self._errorLabel.config(text="")
            arraySize = int(self._numberValue.get())
            listOfThreads = []
            # pasirinktas nuoseklus vykdymas
            if self._optionsMenuValue[0].get() == 1:
                thr = threading.Thread(target=self._actions.doActionsNormally, args=(arraySize,), name="Normal")
                listOfThreads.append(thr)
                thr.start()
            # pasirinktas Threadingo vykdymas
            if self._optionsMenuValue[1].get() == 1:
                thr = threading.Thread(target=self._actions.doActionsOnThreads,
                                       args=(arraySize, int(self._threadValue.get())), name="Threading")
                listOfThreads.append(thr)
                thr.start()

            for t in listOfThreads:
                t.join()

            for t in listOfThreads:
                # Vykdomas nuoseklus darbas
                if t.name == "Normal":
                    # Pridedamas nuoseklaus darbo pavadinimas kaip X asies reiksme
                    xdata.append(t.name)
                    # Pridedamas nuoseklaus darbo vykdymo laikas kaip Y asies reiksme
                    ydata.append(self._actions.workTimeNormal)
                # Vykdomas Thread'ais paremtas darbas
                elif t.name == "Threading":
                    xdata.append(t.name)
                    ydata.append(self._actions.workTimeOnThread)

            # Sukuriamas diagramos objektas
            diagramData = DiagramData(xtitle="Vykdymo tipas", xdata=xdata, ytitle="Laikas sec.", ydata=ydata)
            # Pakeiciamas langas i diagramos langa, perduodant diagramos duomenis
            self._controller.switch_frame(Constants.WINDOW_GRAPHIC, diagramData)

        self._progressLabel.config(text="")


# Klase paveldi informacija is klases Frame ir WindowUtils
class Graphic(tkx.Frame, WindowUtils):
    def __init__(self, parent, controller):
        tkx.Frame.__init__(self, parent)
        self._controller = controller

    def refresh(self, bundle):
        self._controller.title(Constants.TITLE_GRAPHIC)
        self.clearWindow()

        # Mygtukas atgal, kuris grizta i Home (pries tai buvusi) langa
        backButton = tkx.Button(self, text="<-- ATGAL")
        backButton.pack()
        backButton.config(
            command=lambda: self._controller.switch_frame(Constants.WINDOW_HOME))

        # Jeigu keiciant langa buvo perduoti diagramos duomenys, sugeneruojama diagrama
        if bundle:
            # Vykdomas try/except blokas, kad isvengti diagramos braizymo klaidu:
            # Blogi duomenys, masyvu ilgiu neatitikimas (x asis turi daugiau reiksmiu nei y ir atvirksciai) ir pns.
            try:
                self.generateDiagram(bundle)
            except:
                self.showErrorLabel()
        else:
            self.showErrorLabel()

    def showErrorLabel(self):
        errorLabel = tkx.Label(self, text="Negalima nubraizyti diagramos! tikrinkite duomenis.")
        errorLabel.pack()

    def generateDiagram(self, diagramData):
        # Braizoma diagrama pasinaudojant diagramos duomenimis bei paverciant juos i dictionary
        df1 = DataFrame(diagramData.getDiagramAsDictionary(), columns=[diagramData.xtitle, diagramData.ytitle])

        figure1 = plt.Figure(figsize=(7, 9), dpi=70)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self)
        bar1.get_tk_widget().pack(side=tkx.LEFT, fill=tkx.BOTH)
        df1 = df1[[diagramData.xtitle, diagramData.ytitle]].groupby(diagramData.xtitle).sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Veiksmu vykdymo laikas pagal vykdymo tipa')


# Klase application paveldi informacija is klases Tk
class Application(tkx.Tk):
    def __init__(self, *args, **kwargs):
        tkx.Tk.__init__(self, *args, *kwargs)
        container = tkx.Frame()

        # Frames/langų dictionary
        self._frames = {}

        # Šiuo metu aplikacijoje esantis langas
        self._selected = None
        container.pack(side="top", fill="both", expand=True)
        self.minsize(Constants.MIN_WIDTH, Constants.MIN_HEIGHT)

        self.container = container

        # Programoje egzistuojantys langai
        self._frames[Constants.WINDOW_HOME] = Home(parent=container, controller=self)
        self._frames[Constants.WINDOW_GRAPHIC] = Graphic(parent=container, controller=self)

        # Pradinis aplikacijos langas
        self.switch_frame(Constants.WINDOW_HOME)

    def exit(self):
        "Metodas skirtas baigti programos darba (uzdaryti)"
        self.destroy()

    def switch_frame(self, window_name, bundle=None):
        """Destroys current frame and replaces it with a new one."""

        # Jeigu jau egzistuoja bent vienas langas, jis, t.y. Frame, yra sunaikinamas
        if self._selected is not None:
            self._selected.pack_forget()
            self._selected.grid_forget()

        # Kintamasis "bundle" reikalingas norint perduoti kazkokia informacija is vienos klases i kita,
        # t.y. kintamaji, masyva ar kita info.
        self._selected = self._frames[window_name]
        self._selected.refresh(bundle)
        self._selected.pack()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
