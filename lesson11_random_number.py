from flask import Flask,request
from wtforms import validators,StringField,IntegerField, ValidationError
from flask_wtf import FlaskForm
import re, random

def sum_numb(numb_list):
    s=''
    for i in range(len(numb_list)):
        s+=str(numb_list[i])
    return s


class FlaskRandom(Flask):
    FLASK_RANDOM = 0

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'SECRET',
    WTF_CSRF_ENABLED=False,
)


def num_chekking(form,field):
    if field.data > FlaskRandom.FLASK_RANDOM:
        raise ValidationError (message='ваше число больше')
    if field.data < FlaskRandom.FLASK_RANDOM:
        raise ValidationError (message='ваше число меньше')

class UsersForm(FlaskForm):
    num = IntegerField('num',[validators.InputRequired(), num_chekking])



@app.route('/',methods=['GET'])
def number():
    FlaskRandom.FLASK_RANDOM = random.randint(0, 10)
    return 'Число загадано ' + str(FlaskRandom.FLASK_RANDOM)

@app.route('/guess', methods=['GET', 'POST'])
def lucky_number():
    if request.method == 'POST':
        #print(request.form)
        #print(dict(request.form))
        form = UsersForm(request.form)
        mynumb = re.findall('[\d]', str(dict(request.form).values()))
        mynumb = sum_numb(mynumb)
        #print(form.validate())
        #print(form)
        #print(form.errors)
        if form.validate():
            return ('Вы Угадали число {} !!!\n\nНачните новую игру, с помощью GET запроса'.format(mynumb), 200)

        else:
            if re.search('ваше число меньше',str(form.errors)):
                return 'ваше число меньше'
            if re.search('ваше число больше',str(form.errors)):
                return 'ваше число больше'


if __name__ == '__main__':
    app.run()

