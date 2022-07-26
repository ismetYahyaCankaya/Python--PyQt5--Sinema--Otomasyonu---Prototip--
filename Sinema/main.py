# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow,QDialog,QPushButton, QFileDialog, QDateTimeEdit,QComboBox
from PyQt5 import uic
import img_rc  #cmd'ye pyrcc5 resource.qrc -o resource_rc.py yazmalıyız ki görsellerimizi import edebilelim.
from PyQt5.QtGui import QPixmap
import sqlite3

baglanti=sqlite3.connect("sinema.db")

class seans_ekle(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("seans_ekleme.ui",self)
        self.ana_menu_buton.clicked.connect(self.back_menu)
        self.cikis_buton.clicked.connect(self.cikis)
        self.seans_ekle_buton.clicked.connect(self.seans_olustur)
        self.cursor=baglanti.cursor()
        self.salonListe=[]
        self.salonListe=self.cursor.execute("select salonAd from salonlar") 
        for i in self.salonListe:
            self.salon_bagla_combo_box.addItems(i)
        baglanti.commit()  
    def back_menu(self):
       self.hide()
       self.back_menu_metod=sinema_main()
       self.back_menu_metod.show()
      
    def cikis(self):
        self.hide()
    
    def seans_olustur(self):
        
        seansAd=self.seans_adi_text.text()
        seansTarih=self.seans_tarih_edit.text()
        seansSaat=self.seans_saat_edit.text()
        salon_secimi=self.salon_bagla_combo_box.currentText()
        self.cursor=baglanti.cursor()
        self.cursor.execute("select salonId from salonlar where salonAd=(?)",[salon_secimi])
        salon_index=self.cursor.fetchone()[0]
        baglanti.commit() 
        
        self.cursor=baglanti.cursor()
        self.cursor.execute("INSERT INTO seanslar(seansAd,seansTarih,seansSaat,salonId) VALUES(?,?,?,?)",(seansAd,seansTarih,seansSaat,salon_index)) 
        baglanti.commit()        


class salon_ekle(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("salon_ekleme.ui",self)
        self.ana_menu_buton.clicked.connect(self.back_menu)
        self.cikis_buton.clicked.connect(self.cikis)
        self.salon_ekle_buton.clicked.connect(self.salon_olustur)
       
    def back_menu(self):
       self.hide()
       self.back_menu_metod=sinema_main()
       self.back_menu_metod.show()
      
    def cikis(self):
        self.hide()
        
    def salon_olustur(self):
        self.cursor=baglanti.cursor()
        salon_adi=self.salon_adi_text.text()
        self.cursor.execute("INSERT INTO salonlar(salonAd) VALUES(?)",[salon_adi])
        baglanti.commit()
        

class film_ekle(QDialog):
    def __init__(self):
      super().__init__()
      uic.loadUi("film_ekle.ui", self)
      self.ana_menu_buton.clicked.connect(self.back_menu)
      self.cikis_buton.clicked.connect(self.cikis)
      self.film_tur=['Korku','Gizem','Gerilim','Komedi','Fantastik','Macera','Western'] 
      self.film_turu_combo_box.addItems(self.film_tur)
      self.afis_ekle_buton.clicked.connect(self.resim_sec)
      self.film_ekle_buton.clicked.connect(self.film_olustur)
      self.seans_combo_box.currentIndexChanged.connect(self.seans_zaman_yansit)
      self.cursor=baglanti.cursor()
      self.salonListe=[]
      self.salonListe=self.cursor.execute("select salonAd from salonlar")  
      for i in self.salonListe:
          self.salon_combo_box.addItems(i)    
      self.salon_combo_box.currentIndexChanged.connect(self.yenile)
      baglanti.commit() 
    def back_menu(self):
       self.hide()
       self.back_menu_metod=sinema_main()
       self.back_menu_metod.show()
      
    def cikis(self):
        self.hide()
    
    def resim_sec(self):
        self.img=QFileDialog.getOpenFileName(self, 'Open File','c\\', 'Image files (*.jpg *.png *.jpeg)')
        imagePath=self.img[0]
        pixmap=QPixmap(imagePath)
        self.film_afisi_label.setPixmap(QPixmap(pixmap))
        self.film_afisi_label.setScaledContents(True) 
        self.film_afisi_label.setPixmap(QPixmap(self.img[0]))

        
    def yenile(self):
        self.seans_combo_box.clear()
        self.seansBagliListe=[]
        salonAd = self.salon_combo_box.currentText()
        self.cursor=baglanti.cursor()
        self.cursor.execute("select salonId from salonlar where salonAd=(?)",[salonAd])
        salonId=self.cursor.fetchall()[0]
        baglanti.commit()
        self.cursor=baglanti.cursor()
        self.cursor.execute("select seansAd from seanslar where salonId=(?)",(salonId))
        self.seansBagliListe=self.cursor.fetchall()
        for i in self.seansBagliListe:
            self.seans_combo_box.addItems(i)
        baglanti.commit()
     
    def film_olustur(self):
        film_adi=self.film_ismi_text.text()
        film_turu=self.film_turu_combo_box.currentText()
        yonetmen=self.yonetmen_text.text()
        afis=self.img[0] #?
        film_salon=self.salon_combo_box.currentText()
        film_seans=self.seans_combo_box.currentText()
        self.cursor=baglanti.cursor()
        self.cursor.execute("Insert into filmler(filmAd,filmTuru,filmYonetmen,afis,salonAd,seansAd) values(?,?,?,?,?,?)",(film_adi,film_turu,yonetmen,afis,film_salon,film_seans))
        baglanti.commit()
        
        
    def seans_zaman_yansit(self):
        seansAdi=self.seans_combo_box.currentText()
        self.cursor=baglanti.cursor()
        self.cursor.execute("select seansId from seanslar where seansAd=(?)",[seansAdi])
        seansNo=self.cursor.fetchone()[0]
        print(seansNo)
        baglanti.commit()
        self.cursor=baglanti.cursor()
        self.cursor.execute("select seansTarih,seansSaat from seanslar where seansId=(?)",[seansNo])
        seansBilgi=self.cursor.fetchall()
        baglanti.commit()
        self.seans_bilgi.setText(str(seansBilgi))

        
class sinema_main(QMainWindow):
  def __init__(self):
      super().__init__()
      uic.loadUi("sinema.ui", self)
      self.film_ekle.clicked.connect(self.film_ekleme)
      self.salon_ekle.clicked.connect(self.salon_ekleme)
      self.seans_ekle.clicked.connect(self.seans_ekleme)
      
  def film_ekleme(self):
      self.hide()
      self.film_Ekle = film_ekle()
      self.film_Ekle.show()
      
  def salon_ekleme(self):
      self.hide()
      self.salon_Ekle = salon_ekle()
      self.salon_Ekle.show()
      
  def seans_ekleme(self):
      self.hide()
      self.seans_Ekle = seans_ekle()
      self.seans_Ekle.show()   


app = QApplication(sys.argv)
Sinema_main = sinema_main()
Sinema_main.show()
app.exec_()      

