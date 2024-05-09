import pymongo
#from pymongo import MongoClient, auth
import requests
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
from tqdm import tqdm
from PyQt5.QtCore import QBasicTimer
import random
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog, QFormLayout, QVBoxLayout,QApplication
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QMessageBox
from time import sleep, time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
global all_prices ,date,host, list_of_product ,list,usernamee,queue_car,gate_id,list_of_product_in_queue,products_in_vcart
host = 'https://hypermarket1.herokuapp.com'
list_of_product = []
in_queue=0
products_in_vcart=[]
all_prices = []
queue_car=[]
#gate_id='61d0cade1aa7f515930a44c6'
gate_id='62d2bb48a77b24fa2ad61d85'
#time_date=datetime.datetime.now()
#date=time_date.strftime("%d/%m/%Y")

def connection_database(name):
    global pro
    url = "mongodb+srv://hypercashier:Hyper-Cashier@hypermarket.w5w9n.mongodb.net/hypermarket"
    myclient = pymongo.MongoClient(url)
    mydb = myclient["Hypermarket"]
    mycol = mydb["products"]
    pro = mycol.find_one({'name': name})
def print_option(text,type):
    defaultfont = QtGui.QFont('Arial', 13)
    msg = QMessageBox()
    msg.setFont(defaultfont)
    msg.setWindowIcon(QIcon("image/shopping-cart.png"))
    msg.setIcon(type)
    msg.setText(text)
    msg.setWindowTitle("Message")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('ui/login2.ui', self)
        self.show()
        self.setWindowTitle("Supermarket")
        self.setWindowIcon(QIcon("image/shopping-cart.png"))
        self.submit.clicked.connect(self.switch)
        self.sign_up.clicked.connect(self.open_signup)
        self.window2=None
        self.window3= None
        self.images_icons()
    def images_icons(self):
        pixmap1 = QPixmap('image/grocery-cart.png')
        pixmap_resized = pixmap1.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
        self.cart_label.setPixmap(pixmap_resized)
        pixmap3 = QPixmap('image/LOG.png')
        pixmap_resized3 = pixmap3.scaled(350, 350, QtCore.Qt.KeepAspectRatio)
        self.label_log.setPixmap(pixmap_resized3)
    def switch(self):
        username=self.lineEdit_username_2.text()
        password=self.lineEdit_pass_2.text()
        if len(username)==0 or len(password)==0:
            print_option("Please Enter all Fields ",QMessageBox.Warning)
        else:
            global usernamee
            usernamee=username
            data = {'username': username,'password':str(password)}
            self.httpreq_login(data)
    def httpreq_login(self, data):
        global tokenn
        host = 'http://hypermarket-project.herokuapp.com'
        endpoint = '/cashier/login'
        query = '?id=' + gate_id
        url = host + endpoint + query
        try:
            response = requests.post(url, data)
            if response.status_code == 200:
                token = response.json()
                tokenn = token['token']
                #print(tokenn)
                self.window3 = Wait()
                self.close()
                self.window3.show()
            else :
                print_option("Username or Password not correct", QMessageBox.Warning)
        except:
            print_option("Error connection", QMessageBox.Warning)
    def open_signup(self):
        self.window3 = Signup()
        self.close()
        self.window3.show()
class Signup(QtWidgets.QMainWindow):
    def __init__(self):
        super(Signup, self).__init__()
        uic.loadUi('ui/sign_up2.ui', self)
        self.show()
        self.setWindowTitle("Supermarket")
        self.setWindowIcon(QIcon("image/shopping-cart.png"))
        self.submit_singup.clicked.connect(self.form_singup)
        self.login_back.clicked.connect(self.login_b)
        self.window1=None
        self.image_icons()
    def image_icons(self):
        pixmap=QPixmap('image/grocery-cart.png')
        pixmap_resized = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label_3.setPixmap(pixmap_resized)
        pixmap3 = QPixmap('image/sign.png')
        pixmap_resized3 = pixmap3.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.label_sign.setPixmap(pixmap_resized3)
    def form_singup(self):
        name = self.name.text()
        username = self.username.text()
        pass1 = self.password1.text()
        pass2 = self.password2.text()
        shift_date = self.shift_date.currentText()
        if len(name)==0 or len(username)==0 or len(pass1)==0:
            print_option("Please Enter all Fields ",QMessageBox.Warning)
        else:
            if pass1 != pass2  :
                print_option("confirm password not correct ", QMessageBox.Warning)
            else:
                data = {'name': name, 'shift': shift_date, 'username': username, 'password': pass1}
                self.httpreq_signup(data)
    def httpreq_signup(self, data):
        host = 'http://hypermarket-project.herokuapp.com'
        endpoint = '/cashier/register'
        url = host + endpoint
        response = requests.post(url, data)
        if response.status_code == 200:
            self.window3 = Login()
            self.close()
            self.window3.show()
            print_option("Registration completed successfully Please login ", QMessageBox.Information)
        else:
            print_option("Error confirm ", QMessageBox.Warning)
    def login_b(self):
        self.window1 = Login()
        self.close()
        self.window1.show()
class Wait(QtWidgets.QMainWindow):
    def __init__(self):
        super(Wait, self).__init__()
        uic.loadUi('ui/new.ui', self)
        self.show()
        self.setWindowTitle("Supermarket")
        self.setWindowIcon(QIcon("image/shopping-cart.png"))
        global list,index_of_product
        list = []
        index_of_product=0
        self.sum_price.display(sum(all_prices))
        self.tabWidget.tabBar().setVisible(False)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 135)
        self.tableWidget.setColumnWidth(2, 135)
        self.tableWidget.setColumnWidth(3, 220)
        self.tableWidget.setColumnWidth(4, 10)
        self.tableWidgett.setColumnWidth(0, 190)
        self.tableWidgett.setColumnWidth(1, 160)
        self.tableWidgett.setColumnWidth(2, 160)
        self.tableWidgett.setColumnWidth(3, 200)
        self.tableWidgett.setColumnWidth(4, 10)
        self.image_icons()
        self.tabWidget.setCurrentIndex(0)
        #self.label_username.setText(usernamee)
        self.buttons()
    def add_products_car_in_checkout(self):
        list=0
        sum=0
        #print(products_in_vcart)
        try:
            if len(products_in_vcart)==0:
                self.open_car_check()
                print_option("No product in car ", QMessageBox.Warning)
            else:
                #print(products_in_vcart)
                self.tabWidget.setCurrentIndex(4)

                row = 0
                self.total=0
                self.tableWid.setRowCount(len(products_in_vcart) )
                for n in products_in_vcart:
                    sum=n['price']*n['quantity']
                    self.tableWid.setItem(row, 0, QtWidgets.QTableWidgetItem(str(n['name'])))
                    self.tableWid.setItem(row, 1, QtWidgets.QTableWidgetItem(str(n['quantity'])))
                    self.tableWid.setItem(row, 2, QtWidgets.QTableWidgetItem(str(sum)))
                    self.total+=sum
                    row += 1
                self.total_price.setText("The total price = {total_sum}".format(total_sum = self.total))
                #self.ok.clicked.connect( lambda : self.show_price(self.total))
        except Exception as e:print(e)
    def add_product_in_checkout(self):
        global total
        total = 0
        if len(list_of_product)==0:
            self.open_man_check()
            print_option("No product is selected", QMessageBox.Warning)
        else:
            self.tabWidget.setCurrentIndex(4)

            row = 0
            self.tableWid.setRowCount(len(list_of_product))
            for n in list_of_product:
                self.tableWid.setItem(row, 0, QtWidgets.QTableWidgetItem(str(n[0])))
                self.tableWid.setItem(row, 1, QtWidgets.QTableWidgetItem(str(n[1])))
                self.tableWid.setItem(row, 2, QtWidgets.QTableWidgetItem(str(n[3])))
                total+=n[3]
                row += 1
            self.total_price.setText("The total price = {total_sum}".format(total_sum = total))
            #self.ok.clicked.connect( lambda : self.show_price(total))
            #self.total=0
    def show_price(self):
        sum=0
        try:
            if len(list_of_product)==0 and len(products_in_vcart) !=0 :
                for j in products_in_vcart:
                    sum += j['price']*j['quantity']
                    self.tableWidgett.setRowCount(0)
                    host = 'http://hypermarket-project.herokuapp.com'
                    endpoint = '/gateway/checkout'
                    query = '?gateway='+ gate_id
                    import json
                    url = host + endpoint + query
                    id_vcart=id
                    #print(id_vcart)
                    data={'id':id_vcart}
                    #print(data)
                    response = requests.put(url,headers={'Authorization': "Bearer {}".format(tokenn)},data=data)
                    ret = response.json()
                    if response.status_code==200:
                        self.tableWidgett.setRowCount(0)
                        self.tabWidget.setCurrentIndex(0)
                        index_vcartt=self.queue.currentIndex()
                        self.queue.removeItem( index_vcartt)
                    else:
                        print_option("Error in checkout", QMessageBox.Warning)
            else:
                for i in list_of_product:
                    sum+=i[3]
            value_in_lcd=self.sum_price.value()
            self.sum_price.display(value_in_lcd+sum)
            self.tableWid.setRowCount(0)
            self.tableWidget.setRowCount(0)
            list_of_product.clear()
            list.clear()
            products_in_vcart.clear()
            self.tabWidget.setCurrentIndex(0)
        except Exception as e:print(e)
    def final_check(self):
        if len(list_of_product)==0:
            self.add_products_car_in_checkout()
        else:
            self.add_product_in_checkout()
    def cancel_checkout(self):
        self.tabWidget.setCurrentIndex(0)
        self.tableWidget.setRowCount(0)
        list_of_product.clear()
    def buttons(self):
        self.ok.clicked.connect(self.show_price)
        self.refresh.clicked.connect(self.refresh_queue)
        self.add_product.clicked.connect(self.insert_product)
        self.update_product.clicked.connect(self.updat_product)
        self.delete_product.clicked.connect(self.delet_pro)
        self.cancel.clicked.connect(self.cancel_checkout)
        self.car_checkout.clicked.connect(self.final_check)
        #self.refresh.clicked.connect(self.refresh_queue)
        self.number_submit.clicked.connect(self.queue_number)
        self.queue_submit.clicked.connect(self.queue_number)
        self.man_checkout.clicked.connect(self.final_check)
        self.man_check.clicked.connect(self.open_man_check)
        self.car_check.clicked.connect(self.open_car_check)
        self.butt_products.clicked.connect(self.open_products)
        self.search_product.clicked.connect(self.view_info_product)
        self.close_view.clicked.connect(self.open_man_check)
        self.cancel_car_check.clicked.connect(self.open_man_check)
        self.make_change_product.clicked.connect(self.make_pro_change)
        self.cancel_product.clicked.connect(self.open_man_check)
        self.logout.clicked.connect(self.log_out)
        self.add_sale.clicked.connect(self.add_in_list)
    def log_out(self):
        host = 'http://hypermarket-project.herokuapp.com'
        endpoint = '/cashier/logout'
        query = '?id=' + gate_id
        url = host + endpoint + query
        res=requests.post(url,headers={'Authorization': "Bearer {}".format(tokenn)})
        if res.status_code==200:
            self.window = Login()
            self.close()
            self.window.show()
        else:
            print_option("Error", QMessageBox.Information)
    def image_icons(self):
        #--------------------------  icons and image global  -------------------------------------
        pixmap1 = QPixmap('image/cart.png')
        pixmap_resized = pixmap1.scaled(140, 140, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap_resized)
        self.search_product.setIcon(QIcon('image/search.png'))
        self.search_product.setIconSize(QtCore.QSize(20, 20))
        #--------------------------  products option  -------------------------------------
        self.butt_products.setIcon(QIcon('image/products.png'))
        self.butt_products.setIconSize(QtCore.QSize(40, 40))
        self.add_product.setIcon(QIcon('image/add.png'))
        self.add_product.setIconSize(QtCore.QSize(20, 20))
        self.delete_product.setIcon(QIcon('image/delete.png'))
        self.delete_product.setIconSize(QtCore.QSize(20, 20))
        self.update_product.setIcon(QIcon('image/update.png'))
        self.update_product.setIconSize(QtCore.QSize(20, 20))
        self.cancel_product.setIcon(QIcon('image/cancel.png'))
        self.cancel_product .setIconSize(QtCore.QSize(20, 20))
        #--------------------------  manual checkout -------------------------------------
        self.add_sale.setIcon(QIcon('image/add.png'))
        self.add_sale.setIconSize(QtCore.QSize(20, 20))
        self.man_checkout.setIcon(QIcon('image/checko.png'))
        self.man_checkout.setIconSize(QtCore.QSize(20, 20))
        self.cancel_man_check.setIcon(QIcon('image/cancel.png'))
        self.cancel_man_check.setIconSize(QtCore.QSize(20, 20))
        self.man_check.setIcon(QIcon('image/cashier.png'))
        self.man_check.setIconSize(QtCore.QSize(40, 40))
        #--------------------------  car checkout -------------------------------------
        self.car_check.setIcon(QIcon('image/checkout.png'))
        self.car_check.setIconSize(QtCore.QSize(40, 40))
        self.car_checkout.setIcon(QIcon('image/checko.png'))
        self.car_checkout.setIconSize(QtCore.QSize(20, 20))
        self.number_submit.setIcon(QIcon('image/submit.png'))
        self.number_submit.setIconSize(QtCore.QSize(15, 15))
        self.refresh.setIcon(QIcon('image/refresh.png'))
        self.refresh.setIconSize(QtCore.QSize(15, 15))
        self.queue_submit.setIcon(QIcon('image/submit.png'))
        self.queue_submit.setIconSize(QtCore.QSize(15, 15))
        self.cancel_car_check.setIcon(QIcon('image/cancel.png'))
        self.cancel_car_check.setIconSize(QtCore.QSize(20, 20))
        #-------------------------- button view-------------------------------------
        self.make_change_product.setIcon(QIcon('image/manage.png'))
        self.make_change_product.setIconSize(QtCore.QSize(20, 20))
        self.close_view.setIcon(QIcon('image/cancel.png'))
        self.close_view.setIconSize(QtCore.QSize(20, 20))
    def open_man_check(self):
        self.tabWidget.setCurrentIndex(0)
    def open_car_check(self):
        self.tabWidget.setCurrentIndex(1)
    def open_products(self):
        self.tabWidget.setCurrentIndex(2)
    def view_info_product(self):
        name = self.search_pro.text()
        if len(name) == 0:
            print_option("Please enter product name ", QMessageBox.Warning)
        else:
            try:
                url = "mongodb+srv://hypercashier:Hyper-Cashier@hypermarket.w5w9n.mongodb.net/hypermarket"
                myclient = pymongo.MongoClient(url)
                mydb = myclient["Hypermarket"]
                mycol = mydb["products"]
                global pro
                pro=mycol.find_one({'name':name})
                if pro is None:
                    print_option("Please enter vaild product ", QMessageBox.Warning)
                    self.search_pro.setText('')
                else:
                    self.tabWidget.setCurrentIndex(3)
                    self.product_name.setText(pro['name'])
                    self.product_quantity.setText(str(pro['quantity']))
                    self.product_weight.setText(str(pro['weight']))
                    self.product_price.setText(str(pro['price']))
                    self.product_barcode.setText(str(pro['barcode']))
                    self.product_image.setText(pro['image'])
                    self.search_pro.setText('')
            except Exception as  e:
                self.tabWidget.setCurrentIndex(0)

                print_option("Error connection ", QMessageBox.Warning)
    def make_pro_change(self):
        self.tabWidget.setCurrentIndex(2)
        self.product_name_2.setText(pro['name'])
        self.product_quantity_2.setText(str(pro['quantity']))
        self.product_weight_2.setText(str(pro['weight']))
        self.product_price_2.setText(str(pro['price']))
        self.product_barcode_2.setText(str(pro['barcode']))
        self.product_image_2.setText(pro['image'])
        self.search_pro.setText('')
    def add_in_list(self):
        row=0
        name = self.name_product.text()
        quin = self.doubleSpinBox.value()
        if name is None or quin ==0:
            print_option("Please fill all the fields ",QMessageBox.Warning)
        else:
            try:
                connection_database(name)
                if pro is None:
                    print_option("Please enter vaild product ",QMessageBox.Warning)
                    self.name_product.clear()
                    self.doubleSpinBox.clear()
                else:
                    price=pro['price']
                    if list_of_product == []:
                        self.add_product_in_listview(name,price,quin)
                    else:
                        if name not in list :
                            self.add_product_in_listview(name,price,quin)
                        elif name in list:
                            print_option("This product is in list ", QMessageBox.Warning)
                            #print_option("This product vusjskhskshsfhhks ", QMessageBox.Warning)

                        else:
                            print_option("This product is d ", QMessageBox.Warning)

            except:
                print_option("Error connection", QMessageBox.Warning)

        #self.tableWidget.setColumnCount(len(l))
    def add_product_in_listview(self,name,price,quin):
        row = 0
        total_price_product = price * quin
        self.tableWidget.setRowCount(len(list_of_product) + 1)
        list_of_product.append([name, quin, price, total_price_product])
        list.append(name)
        for n in list_of_product:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(n[0]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(n[2])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(n[3])))
            self.delete = QPushButton()
            self.delete.clicked.connect(self.delete_row)
            self.tableWidget.setCellWidget(row, 4, self.delete)
            self.delete.setIcon(QIcon('image/delete.png'))
            self.delete.setStyleSheet("background-color:white")
            self.delete.setIconSize(QtCore.QSize(20, 20))
            self.delete.setMaximumSize(50, 20)
            self.spinbox=QDoubleSpinBox()
            self.tableWidget.setCellWidget(row, 1, self.spinbox)
            self.spinbox.setValue(n[1])
            self.spinbox.setMaximumSize(125,60)
            self.spinbox.valueChanged.connect(self.spin_method)

            row += 1
        self.name_product.clear()
        self.doubleSpinBox.setValue(1)
    def spin_method(self):
        #print(list_of_product)
        widget = QtWidgets.QApplication.focusWidget()
        one_product_edit = self.tableWidget.indexAt(widget.pos())
        if one_product_edit.isValid():
            index_of_product = one_product_edit.row()
            #print(self.spinbox.value())
        list_one_product=list_of_product[index_of_product]
        list_one_product[1]=self.spinbox.value()
        new_total_price=list_one_product[1] * list_one_product[2]
        list_one_product[3]=new_total_price
        self.tableWidget.setItem(index_of_product, 3, QtWidgets.QTableWidgetItem(str(new_total_price)))
        list_one_product=[]

        # setting text to the label
        #print("Value Changed Signal",new_total_price,  list_of_product[index_of_product],list_of_product)
    def delete_row(self):
        try:
            widget = QtWidgets.QApplication.focusWidget()
            one_product_edit = self.tableWidget.indexAt(widget.pos())
            if one_product_edit.isValid():
                print(list_of_product)
                index_of_product = one_product_edit.row()
                list_of_product.pop(index_of_product)
                list.pop(index_of_product)
            button = self.sender()
            if button:
                row = self.tableWidget.indexAt(button.pos()).row()
                self.tableWidget.removeRow(row)
        except Exception as e:
            print(e)
    def showdialog(self):
        defaultfont = QtGui.QFont('Arial',13)

        global total_sum_product
        total_sum_product = 0
        if list_of_product ==[]:
            print_option("There are no products selected ",QMessageBox.Warning)

        else:
            for i in list_of_product:
                total_sum_product += i[3]
            all_prices.append(total_sum_product)
            print(all_prices)
            msg = QMessageBox()
            try:
                self.tableWidget = QtGui.QTableWidget(parentItem)
                self.tableWidget.setGeometry(QtCore.QRect(0, 0, 540, 250))
                self.tableWidget.setObjectName('tableWidget')

                self.tableWidget.setColumnCount(5)
                self.tableWidget.setRowCount(6)
                msg.tableWidget
            except Exception as e:print(e)
            msg.setFont(defaultfont)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon("image/shopping-cart.png"))
            #msg.setStyleSheet("QLabel {min-width: 200px; min-height: 100px; font-size:13pt bold;font-family: Arial;position:center;backgroundcolor : red}")
            msg.setText("The total price = {total_sum}".format(total_sum = total_sum_product))
            msg.setWindowTitle("Total Price")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.option)
            retval = msg.exec_()
    def option(self,i):
        if i.text() == 'OK':
            self.sum_price.display(sum(all_prices))
            list_of_product.clear()
            self.tableWidget.setRowCount(0)
    def clear(self):
        self.product_name_2.setText('')
        self.product_quantity_2.setText('')
        self.product_weight_2.setText('')
        self.product_price_2.setText('')
        self.product_barcode_2.setText('')
        self.product_image_2.setText('')
        self.search_pro.setText('')
    def refresh_queue(self):
        host = 'http://hypermarket-project.herokuapp.com'
        endpoint = '/gateway/refreshqueue'
        query = '?id=' + gate_id
        url = host + endpoint + query
        try:
            response = requests.get(url, headers={'Authorization': "Bearer {}".format(tokenn)})
            ret = response.json()
            global queue
            queue=ret['queue']
            if response.status_code == 200:
                if len(queue) == 0:
                    print_option("No car in queue", QMessageBox.Information)
                else:
                    for i in queue:
                        if i['cart_name'] not in queue_car:
                            self.queue.addItem(i['cart_name'])
                            queue_car.append(i['cart_name'])
                        else:
                            break
            else:
                print_option("Erorr in connectionnnn", QMessageBox.Warning)
        except:
            print_option("Erorr in connection", QMessageBox.Warning)
    def car_num(self):
        x=self.car_number.text()
        if len(self.car_number.text())==0:
            print_option("Please Enter car number ",QMessageBox.Warning)
        elif x.isdigit() == True :
            try:

                host = 'https://hypermarket1.herokuapp.com'
                endpoint = '/vcart'
                query = '?id=' + gate_id
                url = host + endpoint + query
                response = requests.get(url)
                if response.status_code==503:
                    print_option("Error connection ", QMessageBox.Warning)
                else:
                    pass
                #print(response.status_code)
            except:
                print_option("Error connection ", QMessageBox.Warning)


        else:
            print_option("Please enter vaild car number ",QMessageBox.Warning)
    def queue_number(self):
        if self.car_number.text()=='':
            name = self.queue.currentText()
        else:
            name = self.car_number.text()
        if name == ''    :
            print_option("No car name", QMessageBox.Warning)
        else:

            host = 'http://hypermarket-project.herokuapp.com'
            endpoint = '/gateway/refreshqueue'
            query = '?id=' + gate_id
            url = host + endpoint + query
            try:
                response = requests.get(url, headers={'Authorization': "Bearer {}".format(tokenn)})
                ret = response.json()
                queue = ret['queue']
                in_queue=queue
                for i in range(len(in_queue)):
                    if in_queue[i]['cart_name'] == str(name):
                        global id
                        id = in_queue[i]['_id']
                        print(id)
                        endpoint_2 = '/vcart/products'
                        query_2 = '?id=' + id
                        url = host + endpoint_2 + query_2
                        response = requests.get(url)
                        #print(response.json())
                        ret = response.json()
                        pro_in_vcart = ret['Products']
                        print(pro_in_vcart)
                        global products_in_vcart,index_vcart
                        products_in_vcart=pro_in_vcart
                        index_vcart=self.queue.currentIndex()

                        print(index_vcart)
                        break
                    else:
                        print_option("car name not vaild", QMessageBox.Warning)
                        break
            except Exception as e:
                print(e)

            row=0
            try:
                if products_in_vcart==[] or products_in_vcart==0:
                    print_option("No products in cart", QMessageBox.Warning)
                else:
                    self.tableWidgett.setRowCount(len(products_in_vcart))
                    for n in range(len(products_in_vcart)):
                        self.tableWidgett.setItem(row, 0, QtWidgets.QTableWidgetItem(products_in_vcart[n]['name']))
                        self.tableWidgett.setItem(row, 1, QtWidgets.QTableWidgetItem(str(products_in_vcart[n]['quantity'])))
                        self.tableWidgett.setItem(row, 2, QtWidgets.QTableWidgetItem(str(products_in_vcart[n]['price'])))
                        self.tableWidgett.setItem(row, 3, QtWidgets.QTableWidgetItem(str(products_in_vcart[n]['price']*products_in_vcart[n]['quantity'])))
                        self.delete = QPushButton()
                        #self.delete.clicked.connect(self.delete_row)
                        self.tableWidgett.setCellWidget(row, 4, self.delete)
                        self.delete.setIcon(QIcon('image/delete.png'))
                        self.delete.setStyleSheet("background-color:white")
                        self.delete.setIconSize(QtCore.QSize(20, 20))
                        self.delete.setMaximumSize(50, 20)
                        self.spinbox = QDoubleSpinBox()
                        self.tableWidgett.setCellWidget(row, 1, self.spinbox)
                        self.spinbox.setValue(products_in_vcart[n]['quantity'])
                        self.spinbox.setMaximumSize(125, 60)
                        #self.spinbox.valueChanged.connect(self.spin_method)
                        row+=1
                    #self.tableWidgett.setRow(2)
                    self.car_number.setText('')
            except Exception as e:
                print(e)
    def insert_product(self):
        try:
            url = "mongodb+srv://hypercashier:Hyper-Cashier@hypermarket.w5w9n.mongodb.net/hypermarket"
            myclient = pymongo.MongoClient(url)
            mydb = myclient["Hypermarket"]
            mycol = mydb["products"]
            name = self.product_name_2.text()
            barcode = int(self.product_barcode_2.text())
            quantity = int(self.product_quantity_2.text())
            weight = float(self.product_weight_2.text())
            price = float(self.product_price_2.text())
            image = self.product_image_2.text()
            record = {'barcode':barcode,'name':name,'weight':weight,'image':image,'price':price,'quantity':quantity}
            mycol.insert_one(record)
            self.clear()
            #self.message.setText("Product aded successfully")
            print_option("Product aded successfully", QMessageBox.Information)
        except:
            print_option("The data must be entered correctly", QMessageBox.Warning)

            #self.message.setText("The data must be entered correctly")
    def updat_product(self):
        try:
            name = self.search_pro.text()
            url = "mongodb+srv://hypercashier:Hyper-Cashier@hypermarket.w5w9n.mongodb.net/hypermarket"
            myclient = pymongo.MongoClient(url)
            mydb = myclient["Hypermarket"]
            mycol = mydb["products"]
            filter = {'name': name}
            name2 = self.product_name_2.text()
            barcode = int(self.product_barcode_2.text())
            quantity = int(self.product_quantity_2.text())
            weight = float(self.product_weight_2.text())
            price = float(self.product_price_2.text())
            image = self.product_image_2.text()
            record = {"$set": {'barcode': barcode, 'name': name2, 'weight': weight, 'image': image, 'price': price,'quantity': quantity}}
            mycol.update_one(filter, record)
            self.clear()
            #self.message.setText("Product updated successfully")
            print_option("Product updated successfully", QMessageBox.Information)

        except:
            #self.message.setText("Error in Update")
            print_option("Error in Update", QMessageBox.Warning)
    def delet_pro(self):
        try:
            print(self.product_name.text())
            if self.product_name_2.text() == ''  :
                print_option("No correct date entery", QMessageBox.Warning)
            else:
                name = self.search_pro.text()
                url = "mongodb+srv://hypercashier:Hyper-Cashier@hypermarket.w5w9n.mongodb.net/hypermarket"
                myclient = pymongo.MongoClient(url)
                mydb = myclient["Hypermarket"]
                mycol = mydb["products"]
                mycol.delete_one({'name':name})
                self.clear()
                #self.message.setText("Product Deleted successfully")
                print_option("Product Deleted successfully", QMessageBox.Information)
        except Exception as e:print(e)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #mainWin = Login()
    #mainWin =MainWindow()
    mainWin=Wait()
    #mainWin=Car_check()
    #mainWin = View()
    #mainWin =Signup()
    mainWin.show()
    #test.main()
    sys.exit(app.exec_())


