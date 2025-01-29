import pymysql as sql
import sys
import os
import datetime

sql_host='localhost'
sql_user='root'
sql_password=''
sql_database='test'

'''
CREATE TABLE books (
    bookid INT PRIMARY KEY AUTO_INCREMENT,
    bname VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    btype VARCHAR(100) NOT NULL,
    pubyear INT,
    nop INT CHECK (nop > 0),
    noc INT CHECK (noc > 0)
);

CREATE TABLE member (
    memberid INT PRIMARY KEY AUTO_INCREMENT,
    mname VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    mobileno VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE trans (
    transid INT PRIMARY KEY AUTO_INCREMENT,
    memberid INT NOT NULL,
    bookid INT NOT NULL,
    bookstatus ENUM('ISSUED', 'RETURNED', 'LOST') NOT NULL,
    dateiss DATE NOT NULL,
    dateret DATE NOT NULL
);
'''
# code for adding book **********
def addBook():
   mycursor=conn.cursor()
   query="select bookid from books order by bookid desc limit 1"
   mycursor.execute(query)
   row=mycursor.fetchone()
   
   if mycursor.rowcount==0:
      bookno=1
   else:
      bookno=row["bookid"]
      bookno+=1
   print('Book ID :',bookno)
   bname=input('Enter Book Name:')
   author=input('Enter Author Name:')
   publisher=input('Enter Publisher Name:')
   booktype=input('Enter Book Type:')
   publyear=int(input('Enter Publish Year:'))
   nopage=int(input('Enter Number of Pages:'))
   nocopies=int(input('Enter No. of Copies:'))
   query="insert into books values({},'{}','{}','{}','{}',{},{},{})"
   mycursor.execute(query.format(bookno,bname,author,publisher,booktype,publyear,nopage,nocopies))
   resp=input('Do you want to Save Book(Y/N)?')
   if resp in ['Y','y']:
      conn.commit()
      print('Book Save sucessfully!!!')
   
   else:
      conn.rollback()
      print('No Records Saved!!!')
#code for modifying book **********
def modiBook():
   mycursor=conn.cursor()
   bookno=int(input('Enter Book ID:'))
   query="select * from books where bookid={}"
   mycursor.execute(query.format(bookno))
   count=mycursor.rowcount
   if count==0:
      print('Book ID ',bookno,' Not Found!!!')
   else:
      print('Book ID ',bookno,'has Following Details:')
   rows=mycursor.fetchall()
   for row in rows:
      print("BOOK NO :",row["bookid"])
      print("BOOK NAME :",row["bname"])
      print("AUTHOR :",row["author"])
      print("PUBLISHER :",row["publisher"])
      print("BOOK TYPE :",row["btype"])
      print("PUBLISH YEAR :",row["pubyear"])
      print("NUMBER OF PAGES :",row["nop"])
      print("NUMBER OF COPIES:",row["noc"])
      print('------------------------------------------------------')
   c=input('Do You Want to Change Book(Y/N)?')
   if c in ['Y','y']:
      bname=input('Enter Book Name:')
      author=input('Enter Author Name:')
      publisher=input('Enter Publisher Name:')
      booktype=input('Enter Book Type:')
      publyear=int(input('Enter Publish Year:'))
      nopage=int(input('Enter Number of Pages:'))
      nocopies=int(input('Enter No. of Copies:'))
      query="update books set bname='{}',author='{}',publisher='{}',btype='{}',pubyear={},nop={},noc={} where bookid={}"
      mycursor.execute(query.format(bname,author,publisher,booktype,publyear,nopage,nocopies,bookno))
      conn.commit()
      print('Book Changed sucessfully!!!')
   else:
      conn.rollback()
      print('No Records Changed!!!')

#code for deleting book **********
def delBook():
   mycursor=conn.cursor()
   bookno=int(input('Enter Book ID:'))
   query="select * from books where bookid={}"
   mycursor.execute(query.format(bookno))
   count=mycursor.rowcount
   if count==0:
      print('Book ID ',bookno,' Not Found!!!')
   else:
      print('Book ID ',bookno,'has Following Details:')
   rows=mycursor.fetchall()
   for row in rows:
      print("BOOK NO :",row["bookid"])
      print("BOOK NAME :",row["bname"])
      print("AUTHOR :",row["author"])
      print("PUBLISHER :",row["publisher"])
      print("BOOK TYPE :",row["btype"])
      print("PUBLISH YEAR :",row["pubyear"])
      print("NUMBER OF PAGES :",row["nop"])
      print("NUMBER OF COPIES:",row["noc"])
      print('------------------------------------------------------')
   c=input('Do You Want to Delete(Y/N)?')
   if c in ['Y','y']:
      query="delete from books where bookid={}"
      mycursor.execute(query.format(bookno))
      conn.commit()
      print('Book Deleted sucessfully!!!')
   else:
      conn.rollback()
      print('No Records Deleted!!!')

# code for Queries all books ******
def qallBooks():
   mycursor=conn.cursor()
   query="select * from books order by bname asc"
   mycursor.execute(query)
   count=mycursor.rowcount
   if count==0:
      print('No Book Found!!!')

   else:
      print('Books Details are:')
      rows=mycursor.fetchall()
      print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["bookid"]).ljust(7),str(row["bname"]).ljust(25),str(row["author"]).ljust(25),str(row["publisher"]).ljust(25),str(row["btype"]).ljust(20),str(row["pubyear"]).center(12),str(row["nop"]).center(4),str(row["noc"]).center(3))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
            print(132*'=')
 
# code for name wise book
def qnamewiseBook():
   mycursor=conn.cursor()
   bkname=input('Enter Book Name:')
   query="select * from books where lower(bname) like '%{}%'"
   mycursor.execute(query.format(bkname))
   count=mycursor.rowcount
   if count==0:
      print('No Book Found!!!')
   else:
      print('Books Details are:')
   rows=mycursor.fetchall()
   print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
   print(132*'=')
   ctr=1
   for row in rows:
      print(str(row["bookid"]).ljust(7),str(row["bname"]).ljust(25),str(row["author"]).ljust(25),str(row["publisher"]).ljust(25),str(row["btype"]).ljust(20),str(row["pubyear"]).center(12),str(row["nop"]).center(4),str(row["noc"]).center(3))
      ctr+=1
      if ctr%30==0:
         input('Press any key to see more...')
         print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
         print(132*'=')

# code for publisher wise book
def qpublisherBook():
   mycursor=conn.cursor()
   publisher=input('Enter Publisher Name:')
   query="select * from books where lower(publisher) like '%{}%'"
   mycursor.execute(query.format(publisher))
   count=mycursor.rowcount
   if count==0:
      print('No Publisher Found!!!')
   else:
      print('Publisher Details are:')
   rows=mycursor.fetchall()
   print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
   print(132*'=')
   ctr=1
   for row in rows:
      print(str(row["bookid"]).ljust(7),str(row["bname"]).ljust(25),str(row["author"]).ljust(25),str(row["publisher"]).ljust(25),str(row["btype"]).ljust(20),str(row["pubyear"]).center(12),str(row["nop"]).center(4),str(row["noc"]).center(3))
      ctr+=1
      if ctr%30==0:
         input('Press any key to see more...')
         print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
         print(132*'=')

# code for type wise book
def qtypeBook():
   mycursor=conn.cursor()
   btype=input('Enter Book Type:')
   query="select * from books where lower(btype) like '%{}%'"
   mycursor.execute(query.format(btype))
   count=mycursor.rowcount
   if count==0:
      print('No Such Book Found!!!')
   else:
      print('Books Details are:')
   rows=mycursor.fetchall()
   print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
   print(132*'=')
   ctr=1
   for row in rows:
      print(str(row["bookid"]).ljust(7),str(row["bname"]).ljust(25),str(row["author"]).ljust(25),str(row["publisher"]).ljust(25),str(row["btype"]).ljust(20),str(row["pubyear"]).center(12),str(row["nop"]).center(4),str(row["noc"]).center(3))
      ctr+=1
      if ctr%30==0:
         input('Press any key to see more...')
         print("BOOK NO".ljust(7),"BOOK NAME".ljust(25),"AUTHOR".ljust(25),"PUBLISHER".ljust(25),"BOOKTYPE".ljust(20),"PUBLISH YEAR".center(4),"PAGES".center(4),"COPIES".center(3))
         print(132*'=')

#code for adding member
def addMember():
   mycursor=conn.cursor()
   query="select memberid from member order by memberid desc limit 1"
   mycursor.execute(query)
   row=mycursor.fetchone()
   if mycursor.rowcount==0:
      memberno=101
   else:
      memberno=row["memberid"]
      memberno+=1
   print('member ID :',memberno)
   mname=input('Enter member Name:')
   address=input('Enter address:')
   mobileno=input('Enter mobile number:')
   query="insert into member values('{}','{}','{}','{}')"
   mycursor.execute(query.format(memberno,mname,address,mobileno))
   resp=input('Do you want to Save member(Y/N)?')
   if resp in ['Y','y']:
      conn.commit()
      print('member Save sucessfully!!!')
   else:
      conn.rollback()
      print('No Records Saved!!!')

#code for modifying member
def modiMember():
   mycursor=conn.cursor()
   memberno=int(input('Enter member ID:'))
   query="select * from member where memberid={}"
   mycursor.execute(query.format(memberno))
   count=mycursor.rowcount
   if count==0:
      print('member ID ',memberno,' Not Found!!!')
   else:
      print('member ID ',memberno,'has Following Details:')
   rows=mycursor.fetchall()
   print(rows)
   for row in rows:
      print("member NO :",row["memberid"])
      print("member NAME :",row["mname"])
      print("Member address:",row["address"])
      print("Mobile Number :",row["mobileno"])
      print('------------------------------------------------------')
   c=input('Do You Want to Change member(Y/N)?')
   if c in ['Y','y']:
      mname=input('Enter member Name:')
      address=input('Enter address:')
      mobileno=input('Enter mobile number:')
      query="update member set mname='{}',address='{}',mobileno='{}' WHERE memberid={}"
      mycursor.execute(query.format(mname,address,mobileno,memberno))
      conn.commit()
      print('member Changed sucessfully!!!')
   else:
      conn.rollback()
      print('No Records Changed!!!')

#code for deleting member
def delMember():
   mycursor=conn.cursor()
   memberno=int(input('Enter member ID:'))
   query="select * from member where memberid={}"
   mycursor.execute(query.format(memberno))
   count=mycursor.rowcount
   if count==0:
      print('member ID ',memberno,' Not Found!!!')
   else:
      print('member ID ',memberno,'has Following Details:')
   rows=mycursor.fetchall()
   for row in rows:
      print("member NO :",row["memberid"])
      print("member NAME :",row["mname"])
      print("address :",row["address"])
      print("mobile Number :",row["mobileno"])
      print('------------------------------------------------------')
   c=input('Do You Want to Delete(Y/N)?')
   if c in ['Y','y']:
      query="delete from member where memberid={}"
      mycursor.execute(query.format(memberno))
      conn.commit()
      print('member Deleted sucessfully!!!')
   else:
      conn.rollback()
      print('No Records Deleted!!!')

#code for querying all member
def qallMembers():
   mycursor=conn.cursor()
   query="select * from member order by mname asc"
   mycursor.execute(query)
   count=mycursor.rowcount
   if count==0:
      print('No Memeber Found!!!')

   else:
      print('Memebers Details are:')
      rows=mycursor.fetchall()
      print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["memberid"]).ljust(7),str(row["mname"]).ljust(25),str(row["address"]).ljust(25),str(row["mobileno"]).ljust(13))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
            print(132*'=')

#code for querying member ID
def qmemID():
   mycursor=conn.cursor()
   mid=input("Enter the ID of the memeber")
   query="select * from member where lower(memberid) like '%{}%'"
   mycursor.execute(query.format(mid))
   count=mycursor.rowcount
   if count==0:
      print('No Memeber Found!!!')

   else:
      print('Memebers Details are:')
      rows=mycursor.fetchall()
      print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["memberid"]).ljust(7),str(row["mname"]).ljust(25),str(row["address"]).ljust(25),str(row["mobileno"]).ljust(13))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
            print(132*'=')

#code for querying member number
def qmemNumber():
   mycursor=conn.cursor()
   mobilno=input("Enter the number of the memeber")
   query="select * from member where lower(mobileno) like '%{}%'"
   mycursor.execute(query.format(mobilno))
   count=mycursor.rowcount
   if count==0:
      print('No Memeber Found!!!')

   else:
      print('Memebers Details are:')
      rows=mycursor.fetchall()
      print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["memberid"]).ljust(7),str(row["mname"]).ljust(25),str(row["address"]).ljust(25),str(row["mobileno"]).ljust(13))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
            print(132*'=')

#code for querying member name
def qmemName():
   mycursor=conn.cursor()
   mname=input("Enter  the name of member")
   query="select * from member where lower(mname) like '%{}%'"
   mycursor.execute(query.format(mname))
   count=mycursor.rowcount
   if count==0:
      print('No Memeber Found!!!')

   else:
      print('Memebers Details are:')
      rows=mycursor.fetchall()
      print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["memberid"]).ljust(7),str(row["mname"]).ljust(25),str(row["address"]).ljust(25),str(row["mobileno"]).ljust(13))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("MEMBER NO.".ljust(7),"MEMBER NAME".ljust(25),"MEMBER ADDRESS".ljust(25),"MOBLIE NO.".ljust(13))
            print(132*'=')

#code for issue book
def issueBook():
   mycursor=conn.cursor()
   query="select transid from trans order by transid desc limit 1"
   mycursor.execute(query)
   row=mycursor.fetchone()
   
   if mycursor.rowcount==0:
      transno=1
   else:
      transno=row["transid"]
      transno+=1
   print('TRANSACTION ID:',transno)
   mid=int(input('ENTER THE MEMBER ID:'))
   bid=int(input('Enter Book ID:'))
   issdate=datetime.date.today()
   print("DAY OF ISSUING BOOK:",issdate)
   retdate=input('ENTER THE DATE TO RETURN BOOK (YYYY-MM-DD):')
   bookstatus="ISSUED"
   query="insert into trans values('{}','{}','{}','{}','{}','{}')"
   mycursor.execute(query.format(transno,mid,bid,bookstatus,issdate,retdate))
   resp=input('Do you want to issue book(Y/N)?')
   if resp in ['Y','y']:
      conn.commit()
      print('Transaction sucessfully!!!')

#code for return book
def returnBook():
   mycursor=conn.cursor()
   transid=int(input('ENTER THE TRANSACTION ID:'))
   query="select * from trans where transid={}"
   mycursor.execute(query.format(transid))
   count=mycursor.rowcount
   
   if count==0:
      print('Transaction id',transid,'No Transaction Found!!')
   else:
      print('Transaction id',transid,'has following Details;')
   rows=mycursor.fetchall()
   for row in rows:
      print('TRANSACTION ID:',row["transid"])
      print('THE MEMBER ID:',row['memberid'])
      print('Enter Book ID:',row['bookid'])
      print('THE BOOK STATUS:',row['bookstatus'])
      print('THE DATE OF ISSUE BOOK (YYYY-MM-DD):',row['dateiss'])
      print('THE DATE OF RETURN BOOK (YYYY-MM-DD):',row['dateret'])
   resp=input('Do you want to return the book (Y/N)?')
   if resp in ['Y','y']:
      returnbook='RETURNED'
      query="update trans set bookstatus='{}' where transid='{}'"
      mycursor.execute(query.format(returnbook,transid))
      conn.commit()
      print('Book RETURNED sucessfully!!!')
   else:
      conn.rollback()
      print('Book Not Returned')

#code for lost book
def lostBook():
   mycursor=conn.cursor()
   transid=int(input('ENTER THE TRANSACTION ID:'))
   query="select * from trans where transid={}"
   mycursor.execute(query.format(transid))
   count=mycursor.rowcount
   
   if count==0:
      print('Transaction id',transid,'No Transaction Found!!')
   else:
      print('Transaction id',transid,'has following Details;')
   rows=mycursor.fetchall()
   for row in rows:
      print('TRANSACTION ID:',row["transid"])
      print('THE MEMBER ID:',row['memberid'])
      print('Enter Book ID:',row['bookid'])
      print('THE BOOK STATUS:',row['bookstatus'])
      print('THE DATE OF ISSUE BOOK (YYYY-MM-DD):',row['dateiss'])
      print('THE DATE OF RETURN BOOK (YYYY-MM-DD):',row['dateret'])
   resp=input('Please confirm that the book is lost (Y/N)?')
   if resp in ['Y','y']:
      lostbook='LOST'
      query="update trans set bookstatus='{}' where transid='{}'"
      mycursor.execute(query.format(lostbook,transid))
      conn.commit()
      print('BOOK LOST!!!')
   else:
      conn.rollback()
      print('NO CHANGE MADE')

#code for querying all transaction
def qalltrans():
   mycursor=conn.cursor()
   query="select * from trans order by transid asc"
   mycursor.execute(query)
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for querying transaction ID
def qtransid():
   mycursor=conn.cursor()
   tid=input("ENTER THE TRANSACTION  ID:")
   query="select * from trans where lower(transid) like '%{}%'"
   mycursor.execute(query.format(tid))
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for querying member ID
def qmemberid():
   mycursor=conn.cursor()
   Mid=input("ENTER THE MEMBER  ID:")
   query="select * from trans where lower(memberid) like '%{}%'"
   mycursor.execute(query.format(Mid))
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for querying book ID
def qbookid():
   mycursor=conn.cursor()
   Bid=input("ENTER THE BOOK ID:")
   query="select * from trans where lower(bookid) like '%{}%'"
   mycursor.execute(query.format(Bid))
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for querying book issue
def qbookiss():
   mycursor=conn.cursor()
   iss="ISSUED"
   query="select * from trans where lower(bookstatus) like '%{}%'"
   mycursor.execute(query.format(iss))
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for querying book return
def qbookret():
   mycursor=conn.cursor()
   ret="RETURNED"
   query="select * from trans where lower(bookstatus) like '%{}%'"
   mycursor.execute(query.format(ret))
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for querying book lost
def qbooklos():
   mycursor=conn.cursor()
   ret="LOST"
   query="select * from trans where lower(bookstatus) like '%{}%'"
   mycursor.execute(query.format(ret))
   count=mycursor.rowcount
   if count==0:
      print('No Transaction Found!!!')

   else:
      print('Transaction Details are:')
      rows=mycursor.fetchall()
      print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
      print(132*'=')
      ctr=1
      for row in rows:
         print(str(row["transid"]).ljust(7),str(row["memberid"]).ljust(7),str(row["bookid"]).ljust(7),str(row["bookstatus"]).ljust(10),str(row["dateiss"]).ljust(8),str(row["dateret"]).ljust(8))
         ctr+=1
         if ctr%30==0:
            input('Press any key to see more...')
            print("TRANSACTION ID".ljust(7),"MEMBER ID".ljust(7),"BOOK ID".ljust(7),"BOOK STATUS".ljust(10),"DATE ISSUED".ljust(8),"DATE TO RETURN".ljust(8))
            print(132*'=')

#code for how to use
def howtoUse():
   print('\n\n\n\n~~~~~~')
   print('H O W T O U S E ')
   print('*******')
   print('1.How To Use Book Menu.......')
   print('2.How To Use Member Menu.....')
   print('3.How To Use Transactions....')
   print('4.Exit............')
   ch=int(input('Enter Your Choice:'))
   if ch==1:
      print('\n*******')
      print('H O W  T O  U S E  B O O K M E N U')
      print('##################')
      print('1.How To Add New Book....')
      print('2.How To Modify Book.....')
      print('3.How To Delete Book.....')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         print('Enter Book Name:')
         print('Enter Author Name:')
         print('Enter Publisher Name:')
         print('Enter Book Type:')
         print('Enter Publish Year:')
         print('Enter Number of Pages:')
         print('Enter No. of Copies:')
      elif ch1==2:
         print('Enter Book Name:')
         print('Enter Author Name:')
         print('Enter Publisher Name:')
         print('Enter Book Type:')
         print('Enter Publish Year:')
         print('Enter Number of Pages:')
         print('Enter No. of Copies:')
      elif ch1==3:
         print('ENTER THE BOOK ID')
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
         mainmenu()   
   elif ch==2:
      print('\n*******')
      print('H O W T O U S E M E M B E R M E N U')
      print('#####################')
      print('1.How To Add New Member....')
      print('2.How To Modify Member.....')
      print('3.How To Delete Member.....')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         print('Enter member Name:')
         print('Enter address:')
         print('Enter mobile number:')
      elif ch1==2:
         print('Enter member Name:')
         print('Enter address:')
         print('Enter mobile number:')
      elif ch1==3:
         print('ENTER MEMBER ID')
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
      mainmenu()
   elif ch==3:
      print('\n***********')
      print('T R A N S A C T I O N M E N U')
      print('###############################')
      print('1.How To Issue Book....')
      print('2.How To Return Book.....')
      print('3.What  to Do If Book Lost.....')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         print('ENTER THE MEMBER ID:')
         print('Enter Book ID:')
         print('ENTER THE DATE TO  RETURN BOOK')
      elif ch1==2:
         print('ENTER THE TRANSCATION ID')
      elif ch1==3:
         print('ENTER THE TRANSCATION ID AND CONTACT THE LIBRARY INCHARGE')
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
      mainmenu()
   elif ch==4:
      status=input('Dou you realy want to Quit/Exit(Y/N)...?')
      if status in ['Y','y']:
         sys.exit()
      else:
         pass
   else:
      print('Wrong Choice!!! Try Again!!!')


#Code for mainmenu*******
def mainmenu():
   print('\n\n\n\n~~~~~~')
   print('M A I N M E N U')
   print('*******')
   print('1.Book Menu.......')
   print('2.Member Menu.....')
   print('3.Transactions....')
   print('4.Queries.........')
   print('5.Utilities.......')
   print('6.Help............')
   print('7.Exit............')
   ch=int(input('Enter Your Choice:'))
   if ch==1:
      print('\n*******')
      print('B O O K M E N U')
      print('##################')
      print('1.Add New Book....')
      print('2.Modify Book.....')
      print('3.Delete Book.....')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         addBook()
      elif ch1==2:
         modiBook()
      elif ch1==3:
         delBook()
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
         mainmenu()
   elif ch==2:
      print('\n*******')
      print('M E M B E R M E N U')
      print('#####################')
      print('1.Add New Member....')
      print('2.Modify Member.....')
      print('3.Delete Member.....')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         addMember()
      elif ch1==2:
         modiMember()
      elif ch1==3:
         delMember()
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
      mainmenu()
   elif ch==3:
      print('\n***********')
      print('T R A N S A C T I O N M E N U')
      print('###############################')
      print('1.Issue Book....')
      print('2.Return Book.....')
      print('3.Lost Book.....')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         issueBook()
      elif ch1==2:
         returnBook()
      elif ch1==3:
         lostBook()
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
      mainmenu()
   elif ch==4:
      print('\n*******')
      print('Q U E R Y M E N U')
      print('###################')
      print('-------Books---------')
      print('1.All Books Alphabetical')
      print('2.Specific Book Name Wise')
      print('3.Book Publisher Wise')
      print('4.Type Wise')
      print('-------Member------------')
      print('5.All Members Alphabetical')
      print('6.Member ID Wise')
      print('7.Member Number Wise')
      print('8.Member Name Wise')
      print('-------Transaction----------')
      print('9.ALL Transaction')
      print('10.Transaction ID Wise')
      print('11.Transaction Member ID Wise')
      print('12.Transaction Book ID ')
      print('13.Transaction Book Issued wise')
      print('14.Transaction Book Returned wise')
      print('15.Transaction Book Lost wise')
      print('16.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         qallBooks()
      elif ch1==2:
         qnamewiseBook()
      elif ch1==3:
         qpublisherBook()
      elif ch1==4:
         qtypeBook()
      elif ch1==5:
         qallMembers()
      elif ch1==6:
         qmemID()
      elif ch1==7:
         qmemNumber()
      elif ch1==8:
         qmemName()
      elif ch1==9:
         qalltrans()
      elif ch1==10:
         qtransid()
      elif ch1==11:
         qmemberid()
      elif ch1==12:
         qbookid()
      elif ch1==13:
         qbookiss()
      elif ch1==14:
         qbookret()
      elif ch1==15:
         qbooklos()
      elif ch1==16:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
         mainmenu()
   elif ch==5:
      print('\n*********')
      print('U T I L I T Y M E N U')
      print('#######################')
      print('1.Calculator....')
      print('2.Notepad.......')
      print('3.Paint.........')
      print('4.Back to Main....')
      ch1=int(input('Enter Your Choice:'))
      if ch1==1:
         os.system('calc')
      elif ch1==2:
         os.system('notepad')
      elif ch1==3:
         os.system('mspaint')
      elif ch1==4:
         mainmenu()
      else:
         print('Wrong Choice!!!, Back to Main')
         mainmenu()
       
   elif ch==6:
      howtoUse()
      pass
   elif ch==7:
      status=input('Dou you realy want to Quit/Exit(Y/N)...?')
      if status in ['Y','y']:
         sys.exit()
      else:
         pass
   else:
      print('Wrong Choice!!! Try Again!!!')
   
conn=sql.connect(user=sql_user,password=sql_password,host=sql_host,database=sql_database,cursorclass=sql.cursors.DictCursor)
while True:
   mainmenu()
