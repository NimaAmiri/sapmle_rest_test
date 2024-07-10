import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    send_from_directory,
    redirect,
)
import os

app = Flask(__name__, template_folder='templates')

gpids = []
gpnames = []


@app.route('/')
def index():
    return render_template('index.html', gpids=gpids, gpnames = gpnames)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/add/gpid', methods=['POST'])
def add_gpid():
    gpid = request.form['gpid']
    gpids.append(gpid)
    gpname = request.form['gpname']
    gpnames.append(gpname)  
    return redirect(url_for('index'))

@app.route('/add/gpname', methods=['POST'])
def add_gpname():
    gpname = request.form['gpname']
    gpnames.append(gpname)            
    return redirect(url_for('index'))


@app.route('/remove/<int:index>')
def remove(index):
    del gpids[index-1]
    del gpnames[index-1]
    return redirect(url_for('index'))

 
@app.route('/download_gpids')
def download():
    df = pd.DataFrame({'gpid_id': list(range(len(gpids))), 'gpid': gpids, 'gp_name': gpnames})
    df.to_excel('gpids.xlsx')
    return send_from_directory('.', 'gpids.xlsx')

if __name__ == '__main__' :
    app.run(debug=True)
