from flask import Flask, render_template

from app import app


@app.route('/sitemap/')
def sitemap():
    return render_template('sitemap.xml')
