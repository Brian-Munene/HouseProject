from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

#File imports
from routes import app

@app.route('/')
def index():
    return render_template('home.html')
