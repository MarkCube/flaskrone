from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash

from flask.views import View


class FlaskrView(View):

    def dispatch_request(self):
        cur =g.db.execute('select title, text from entries order by id desc')
        entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
        return render_template('show_entries.html', entries = entries)


class AddEntry(View):

    def dispatch_request(self):
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into entries (title,text) values (?,?)', [request.form['title'],request.form['text']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))



class Login(View):
    def login(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Invalid Username'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        return render_template('login.html', error=error)


class Logout(View):
    def logout(self):
        session.pop('logged_in',None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))
