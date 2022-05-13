import datetime
import sqlite3
from flask import Flask, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


app = Flask(__name__)


connection = sqlite3.connect("news.db", check_same_thread=False)
cursor = connection.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS news(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR NOT NULL,
                    description VARCHAR NOT NULL,
                    category VARCHAR NOT NULL,
                    date VARCHAR NOT NULL,
                    author VARCHAR NOT NULL
                    )""")

connection.commit()

class Account:

    @staticmethod
    def _get_local_time():
        return datetime.date.today()


    def __db_operate(self, op_title, op_description, op_category, op_date, op_author):

        cursor.execute("""INSERT INTO news(date, title, description, category,  author)
                            VALUES
                            (?,?,?,?,?)""",(op_title, op_description, op_category, op_date, op_author))
        connection.commit()


    def __db_delete(self, del_uid):

        cursor.execute("""DELETE FROM news
                            WHERE id = ?""",(del_uid,))
        connection.commit()


    def __db_change_data(self, ch_uid, ch_title, ch_description, ch_category,ch_author):
        cursor.execute("""UPDATE news
            SET title = ?,
            description = ?,
            category = ?,
            author = ?
            WHERE id = ?""",(ch_title,ch_description,ch_category,ch_author,ch_uid,))
        connection.commit()

    def change(self, new_title, new_description, new_category, new_author, uid):
        self.__db_change_data(uid,new_title,new_description,new_category,new_author)


    def add(self, title, description, category,  author):
        self.__db_operate(self._get_local_time(), title, description, category, author)



    def delete(self, uid):
        self.__db_delete(uid)


    def showallnews(self):
        cursor.execute("""SELECT * FROM news """)
        data = cursor.fetchall()
        return data


    def shownews(self, uid):
        cursor.execute("""SELECT * FROM news WHERE id = ?""",(uid,))
        data = cursor.fetchone()
        return data


acc = Account()

class DeleteForm(FlaskForm):
    id = StringField("შეიყვანეთ წასაშლელი ნიუსის ID")
    submit = SubmitField("წაშლა")
@app.route('/delete/<id>', methods=['GET','POST','DELETE'])
def deleteNews(id) -> 'html':
    acc.delete(id)
    return redirect('/')


@app.route('/')
def newsFeed() -> 'html':
    titles = ('სათაური', 'აღწერა', 'კატეგორია', 'თარიღი', 'ავტორი')  # ვქმნით სათაურებს სვეტებისთვის
    contents = acc.showallnews()
    return render_template('showall.html',
                           the_title='იხილეთ ნიუსები',
                           the_row_titles=titles,
                           the_data=contents)



app.config['SECRET_KEY'] = "mysecretkey"



class AddForm(FlaskForm):
    title = StringField("სათაური",[InputRequired()])
    description = StringField("აღწერა",[InputRequired()])
    category = StringField("კატეგორია",[InputRequired()])
    author = StringField("ავტორი",[InputRequired()])
    submit = SubmitField("დამატება")

@app.route('/add', methods=['GET','POST'])
def addNews() -> 'html':
    title = None
    description = None
    category = None
    author = None
    returnhome = redirect('/')
    form = AddForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        author = form.author.data
        acc.add(title,description,category,author)
        form.title.data = ''
        form.description.data = ''
        form.category.data = ''
        form.author.data = ''
        flash("ნიუსი წარმატებით დაემატა")
    return render_template('add.html',
                           returnhome=returnhome,
                           form=form)


class ChangeForm(FlaskForm):
    title = StringField("სათაური",[InputRequired()])
    description = StringField("აღწერა",[InputRequired()])
    category = StringField("კატეგორია",[InputRequired()])
    author = StringField("ავტორი",[InputRequired()])
    submit = SubmitField("შეცვლა")
@app.route('/change/<id>', methods=['GET','POST','PUT'])
def changeNews(id) -> 'html':

    content = acc.shownews(id)
    titles = ('ID', 'სათაური', 'აღწერა', 'კატეგორია', 'თარიღი', 'ავტორი','ოპერაცია')
    form = ChangeForm()

    title = content[1]
    description = content[2]
    category = content[3]
    author = content[5]
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        author = form.author.data
        acc.change(title,description,category,author,id)
        flash("ნიუსი წარმატებით შეიცვალა")
    return render_template('change.html',
                           the_title='იხილეთ ნიუსები',
                           the_row_titles=titles,
                           the_data=content,
                           form=form,
                           title_to_update=title,
                           description_to_update=description,
                           category_to_update=category,
                           author_to_update=author)



if __name__ == '__main__':
    app.run(debug=True)
