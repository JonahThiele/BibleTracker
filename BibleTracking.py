import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
from matplotlib.axes import Axes
import numpy as np
import sqlite3
from datetime import datetime
from datetime import date
BOOKS_OF_THE_BIBLE = ( 'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
                      'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel',
                      '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles',
                      'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalm','Proverbs',
                      'Ecclesiastes','Song of Solomon','Isaiah','Jeremiah',
                      'Lamentations','Ezekiel','Daniel', 'Hosea','Joel',
                      'Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk',
                      'Zephaniah','Haggai','Zechariah','Malachi','Matthew',
                      'Mark','Luke','John','Acts','Romans','1 Corinthians',
                      '2 Corinthians','Galatians','Ephesians','Philippians',
                      'Colossians','1 Thessalonians','2 Thessalonians',
                      '1 Timothy','2 Timothy','Titus','Philemon','Hebrews',
                      'James','1 Peter','2 Peter','1 John','2 John','3 John',
                      'Jude','Revelation')



class Gui:
    #this is a bad hack I need to figure out a better way to write this
    def startDBConnection(self):

        self.sqliteConnection = sqlite3.connect('bibleInfo.db')
        self.cur = self.sqliteConnection.cursor()
        #handle setting up the connection at some point in time

    def updateInitial(self):
        self.updateAll()

    def __init__(self):
        self.bookAbbrev = {
                "amos": 30,
                "1chron.": 13,
                "2chron.": 14,
                "dan.": 27,
                "deut.": 5,
                "eccles.": 21,
                "esther": 17,
                "exod.": 2,
                "ezek.": 26,
                "ezra": 15,
                "gen.": 1,
                "hab.": 35,
                "hag.": 37,
                "hosea": 28,
                "isa.": 23,
                "jer.": 24,
                "job": 18,
                "joel": 29,
                "jon.": 32,
                "josh.": 6,
                "judg.": 7,
                "1kings": 11,
                "2kings": 12,
                "lam.": 25,
                "lev.": 3,
                "mal.": 39,
                "mic.": 33,
                "nah.":34,
                "neh.": 16,
                "num.": 4,
                "obad.": 31,
                "prov.": 20,
                "ps.": 19,
                "ruth": 8,
                "1sam.": 9,
                "2sam.": 10,
                "song of sol.": 22,
                "zech.": 38,
                "zeph.": 36,
                "acts": 44,
                "col.": 51,
                "1cor.": 46,
                "2cor.": 47,
                "eph.": 49,
                "gal.": 48,
                "heb.": 58,
                "james": 59,
                "john": 43,
                "1john":62,
                "2john":63,
                "3john":64,
                "jude":65,
                "luke":42,
                "mark":41,
                "matt.": 40,
                "1pet.":60,
                "2pet.":61,
                "philem.":57,
                "phil.":50,
                "rev.":66,
                "rom.":45,
                "1thess.": 52,
                "2thess.": 53,
                "1tim.": 54,
                "2tim.": 55,
                "titus": 56}
    
        self.fig = plt.figure(figsize=(10, 5))
        self.gs = GridSpec(nrows=3, ncols=3, wspace=1, hspace=.5)

        self.fig.tight_layout()
        #set up this dummy data  then call the update functions in this constructor
        #percent of the Testaments completed overall
        #eventually make this a click on so you can see how much of each book you have completed
        self.newTestament = self.fig.add_subplot(self.gs[0,0])
        self.newTestament.set_title("% complete of NT")
        self.newTestament.pie([80, 20])
        

        self.oldTestament = self.fig.add_subplot(self.gs[1,0])
        self.oldTestament.set_title("% complete of OT")
        self.oldTestament.pie([80, 20])
         

        #the most recent reading in the table
        self.LastReadings = self.fig.add_subplot(self.gs[2,0])
        self.LastReadings.set_xticks([])
        self.LastReadings.set_yticks([])
        self.LastReadingsText = self.LastReadings.text(0.5, 0.7, "Last Reading:", horizontalalignment="center", fontsize=15)

        #chart of how many verse in past 7 days
        self.VersesDaily = self.fig.add_subplot(self.gs[0,1])
        self.VersesDaily.set_xlabel("last 7 days")
        self.VersesDaily.set_ylabel("Verses per day")
        #figure out the ticks and the other important pieces of code in class hopefully

        self.VersesDaily.plot()

        #top chapters completed
        self.TopChapters = self.fig.add_subplot(self.gs[-2:,1])
        self.TopChapters.set_ylabel("Book")
        self.TopChapters.set_xlabel("Chapters read")

        #plan for the week
        #eventually make this graph a click on to open a custom plan menu
        self.plan = self.fig.add_subplot(self.gs[0,2])
        self.plan.set_xticks([])
        self.plan.set_yticks([])
        self.planText1 = self.plan.text(0.5,0.5, "Plan:", horizontalalignment="center", fontsize=15)
        self.planText2 = self.plan.text(0.1, 0.25, "1 Chapter a day", fontsize=10)

        #reading input
        self.inputV= self.fig.add_subplot(self.gs[1,2])
        self.inputV.set_xticks([])
        self.inputV.set_yticks([])
        self.LabelIn = self.inputV.text(0.5, 0.75, "Input Verses in",horizontalalignment="center", fontsize=10)
        self.Format = self.inputV.text(0.5, 0.60, "CH:VS",horizontalalignment="center", fontsize=10)

        #number representation to work with sql
        self.VerseS = None
        self.VerseE = None
        self.startDBConnection()
        self.updateInitial()

        #set up the book selection
        self.Book2 = None
        self.Book1 = None

        self.RadioBook2Up = False
        self.RadioBook1Up = False
    
    def handleVerseIn(self, text, startingVerse=True):
        components  = text.split(":")
        
        #handle all the book abbreviations so they work with the xml file
        if(len(components) != 2 or  not(components[0].isnumeric()) or not (components[1].isdigit())):
            if startingVerse:
                self.VerseS = None
            else:
                self.VerseE = None
        else:
            fullBook = self.Book2
            if(startingVerse):
                fullBook = self.Book1
            chapter = int(components[0].replace(" ", ""))
            verse = int(components[1].replace(" ", ""))
            #check if the vers combo exists
            cur = self.sqliteConnection.cursor()
            cur.execute("select * from bibleKJV where book = ? and chapter = ? and verse = ?", (fullBook, chapter, verse))
            if(cur.fetchall()):
                if startingVerse:
                    #set the correct number
                    self.VerseS = str(fullBook).rjust(2, '0') + str(chapter).rjust(3,'0') +  str(verse).rjust(3, '0')
                else:
                    self.VerseE = str(fullBook).rjust(2, '0') + str(chapter).rjust(3,'0') +  str(verse).rjust(3, '0')

    def GetPercentOT(self):
        
        self.cur.execute("select (select cast(count(*) as real) from bibleKJV where book > 39 and read = 1) / (select cast(count(*) as real) from bibleKJV where book > 39) as diff")
        
        completed = self.cur.fetchall()
        
        labels = "Completed", "Not Completed"
        percentCompleted = 100 * completed[0][0]
        sizes = [percentCompleted, 100 - percentCompleted]

        self.oldTestament.pie(sizes, labels=labels)

        #display on the chart
        
    def GetPercentNT(self):
        
        self.cur.execute("select (select cast(count(*) as real) from bibleKJV where book < 40 and read = 1) / (select cast(count(*) as real) from bibleKJV where book < 40) as diff") 

        completed = self.cur.fetchall()
        labels = "Completed", "Not Completed"
        percentCompleted = 100 * completed[0][0]
        sizes = [percentCompleted, 100 - percentCompleted]

        self.newTestament.pie(sizes, labels=labels)
    
    def getName(self, book):
        val = BOOKS_OF_THE_BIBLE[book]
        return val
        #display the chart

    def GetTopBooks(self):
        # doesn't get the top %books read, but instead returns the most verses of each book read this function needs to change to sum up everything
        self.cur.execute("select book, count(book) from bibleKJV where read = 1 group by book order by count(book) desc limit 5")

        data = self.cur.fetchall()
        books = []
        verses = []
        bookNames = []
        #iterate through top 5 books
        topbooks = len(data) if len(data) < 5 else 5
        for i in range(topbooks):
            books.append(data[i][0])
            verses.append(data[i][1])

        bookNames = [self.getName(i) for i in books]
        self.TopChapters.barh(books, verses,tick_label=bookNames, color='maroon')

    def GetWeekly(self):
        #fill with empty zeros to handle null from query
        vPerDay = [0] * 8
        
        self.cur.execute("SELECT vsum, vdate FROM VerseHistory WHERE VDATE BETWEEN datetime('now', '-7 day') and datetime('now', 'localtime') order by Vdate desc")
        verses = self.cur.fetchall()
        for verse in verses:
            #conver the sql date to a datetime object
            date_ob = datetime.strptime(verse[1], '%Y-%m-%d').date()
            
            vPerDay[int(str(date.today() - date_ob).split(" ")[0]) - 8] += int(verse[0])

        #graph the correct values
        self.VersesDaily.set_xticks([0, 1, 2, 3, 4 ,5, 6, 7])
        self.VersesDaily.plot([0, 1, 2, 3, 4, 5, 6,7], vPerDay)
    
    def GetLastReading(self):
        # join the tables to get the correct value here
        self.cur.execute("select bibleKJV.verseText, bibleKJV.book, bibleKJV.chapter, bibleKJV.verse from bibleKJV Inner Join VerseHistory on bibleKJV.id=VerseHistory.Vcode2 order by VerseHistory.Vdate desc;")
        lastReading = self.cur.fetchall()
        if self.cur.rowcount < 1:
            pass
        else:
            readingText = lastReading[0][0]
            citationBook = self.getName(lastReading[0][1])
            citationChapter = lastReading[0][2]
            citationVerse = lastReading[0][3]
            fullCitation = str(citationBook) + " " + str(citationChapter) + ":" + str(citationVerse)

            #break on each 20th character
            brokenReading = [readingText[i:i+20] for i in range(0, len(readingText), 20)]
            alignmentOffset = 0.55
            for text in brokenReading:
                self.LastReadingsText = self.LastReadings.text(0.5, alignmentOffset, text, horizontalalignment="center", fontsize=10)
                alignmentOffset -= 0.15
            #add the citation at the end
            self.LastReadingText = self.LastReadings.text(0.5, alignmentOffset,fullCitation, horizontalalignment="center", fontsize=10)
    
    def updateAll(self):
        self.GetPercentOT()
        self.GetPercentNT()
        self.GetTopBooks()
        self.GetWeekly()
        self.GetLastReading()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def VerseEntry(self, event):
         
         #check that this is actually working
         self.cur.execute("select count(*) from bibleKJV where id between ? and ?",(self.VerseS, self.VerseE))

         vsum = self.cur.fetchall()
         self.cur.execute("insert into VerseHistory(Vcode1, Vcode2, Vsum, Vdate) values(?,?,?,DATE('now'))",(self.VerseS, self.VerseE,vsum[0][0]))

         self.sqliteConnection.commit()
         self.cur.execute("update bibleKJV set read = 1 where id between ? and ?", (self.VerseS, self.VerseE))
         self.sqliteConnection.commit()

         #update everything now that we have committed the data
         self.updateAll()
    
    def closedRadioButton2(self, event):
        self.closedRadioButton(bookNum=2)
    
    #this is hacky and stupid but it just works
    def closedRadioButton(self,event="dud",bookNum=1):
        if(bookNum == 1):
            plt.close('BookSelect1')
            self.RadioBook1Up = False
        else:
            plt.close('BookSelect2')
            self.RadioBook2Up = False

    def setBook2(self, label):
        self.Book2 = BOOKS_OF_THE_BIBLE.index(label)

    def setBook1(self, label):
        self.Book1 = BOOKS_OF_THE_BIBLE.index(label)

    def SelectBook2(self, event):
        if( not self.RadioBook2Up):
            self.BookInputFigure2 = plt.figure(num='BookSelect2',figsize=(3,10))
            #set up the radio button to fill the whole window
            radioAxes = self.BookInputFigure2.add_axes([0, 0, 1, 1])
            self.radioBtns2 = RadioButtons(radioAxes, BOOKS_OF_THE_BIBLE)
            SubmitBookButton = self.BookInputFigure2.add_axes([0.55, 0, 0.3, 0.03])
            self.SubmitBookButton2 = Button(SubmitBookButton, 'Select', color="maroon")
            plt.show(block=False)
            self.radioBtns2.on_clicked(self.setBook2)
            #set up so the function closes the window so it is easier for the user to undersand 
            #what is going on
            self.SubmitBookButton2.on_clicked(self.closedRadioButton2)
            self.RadioBook2Up = True

    def SelectBook1(self, event, first=True):
        if( not self.RadioBook1Up):
            #open a new figure and select the right name for the book
            self.BookInputFigure1 = plt.figure(num='BookSelect1',figsize=(3,10))
            #cover the whole of the new figure
            radioAxes = self.BookInputFigure1.add_axes([0, 0, 1, 1])
            self.radioBtns1 = RadioButtons(radioAxes, BOOKS_OF_THE_BIBLE)
            SubmitBookButton = self.BookInputFigure1.add_axes([0.55, 0, 0.3, 0.03])
            self.SubmitBookButton1 = Button(SubmitBookButton, 'Select', color="maroon")
            plt.show(block=False)
            self.radioBtns1.on_clicked(self.setBook1)
            self.SubmitBookButton1.on_clicked(self.closedRadioButton)
            self.RadioBook1Up = True
        
    def CreateOTPies(self):
        self.OTPie = plt.figure(num='OTChapters', figsize=(7, 7))
        self.OTPieGs = GridSpec(nrows=8, ncols=5, wspace=2, hspace=.5)
        #39 books in the OT
        r = 0
        c = 0
        for i in range(39):
            fixedChapter = i + 1
            self.cur.execute("select count(*) from bibleKJV where book = ? and read = 1",(fixedChapter,))
            read = self.cur.fetchall()
            self.cur.execute("select count(*) from bibleKJV where book = ?",(fixedChapter,))
            totalVerses = self.cur.fetchall()
            otPlot = self.OTPie.add_subplot(self.OTPieGs[r,c])
            c += 1
            if(c > 4):
                c = 0
                r += 1
            otPlot.set_title(BOOKS_OF_THE_BIBLE[i])
            completed = (int(read[0][0]) / int(totalVerses[0][0])) * 10
            otPlot.pie([100 - completed, completed])
        plt.show(block=False)

    def CreateNTPies(self):
        self.NTPie = plt.figure(num='NTChapters', figsize=(7, 7))
        self.NTPieGs = GridSpec(nrows=6, ncols=5, wspace=2, hspace=.5)
        #27 books in the NT
        r = 0
        c = 0
        for i in range(27):
            fixedChapter = i + 39
            self.cur.execute("select count(*) from bibleKJV where book = ? and read = 1", (fixedChapter,))
            read = self.cur.fetchall()
            self.cur.execute("select count(*) from bibleKJV where book = ?",(fixedChapter,))
            totalVerses = self.cur.fetchall()
            ntPlot = self.NTPie.add_subplot(self.OTPieGs[r,c])
            c += 1
            if(c > 4):
                c = 0
                r += 1
            ntPlot.set_title(BOOKS_OF_THE_BIBLE[i+39])
            completed = (int(read[0][0]) / int(totalVerses[0][0])) * 10
            ntPlot.pie([100 - completed, completed])
        plt.show(block=False)

    # check if the pie plots have been clicked and if they have open up a new window with pie charts
    # of individual chapters for the OT and NT 
    def checkPieClick(self, event):
        '''print('X: ' + str(event.x))
        print('Y: ' + str(event.y))'''
        #clicked on the new testament
        if((event.x > 153 and event.x < 260) and (event.y > 350 and event.y < 435)):
            self.CreateNTPies()
        #clicked on the old testament
        if((event.x > 153 and event.x < 260) and (event.y < 282 and event.y > 212)):
            self.CreateOTPies()

    def setupInput(self):
        EndVerseAxes = self.fig.add_axes([0.745, 0.40, 0.155, 0.05])
        StartVerseAxes = self.fig.add_axes([0.745, 0.45, 0.155, 0.05])

        self.startingVerse = TextBox(StartVerseAxes, "", initial="starting verse")
        self.startingVerse.on_submit(self.handleVerseIn)

        self.endingVerse = TextBox(EndVerseAxes, "", initial="ending verse")
        self.endingVerse.on_submit(self.handleVerseInEnd)

        #note to place into sql table
        self.notes = self.fig.add_subplot(self.gs[2,2])
        self.notes.set_xticks([])
        self.notes.set_yticks([])
        self.notes.text(0.5, 0.75, "Add Extra Notes",horizontalalignment="center", fontsize=10)

        NotesAxes = self.fig.add_axes([0.745, 0.20, 0.155, 0.05])
        self.verseNotes = TextBox(NotesAxes, "", initial="Notes")

        #add a submit button
        ButtonAxes = self.fig.add_axes([0.765, 0.315, 0.1, 0.075])
        self.subBtn = Button(ButtonAxes, 'submit', color="green")
        self.subBtn.on_clicked(self.VerseEntry)

        #add a quick verse add button
        Book1Button = self.fig.add_axes([0.62, 0.45, 0.12, 0.055])
        self.subB1Btn = Button(Book1Button, 'first book', color="maroon")
        
        self.subB1Btn.on_clicked(self.SelectBook1)

        Book2Button = self.fig.add_axes([0.62, 0.4, 0.12, 0.055])
        self.subB2Btn = Button(Book2Button, 'second book', color="maroon")
        
        self.subB2Btn.on_clicked(self.SelectBook2)
        
        self.fig.suptitle("Bible Tracker")

        #set up click events
        plt.connect("button_press_event", self.checkPieClick)

    def handleVerseInEnd(self,text):
        self.handleVerseIn(text, startingVerse=False)  
    

   #setting up gui and plots
def main():
    qui = Gui()
    qui.setupInput()
    qui.GetWeekly()
    plt.show()

if __name__=="__main__":
    main()

