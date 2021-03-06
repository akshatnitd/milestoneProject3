#!/usr/bin/python

import os
from flask import Flask, render_template, request
from os import path
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if path.exists('env.py'):
    import env


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'milestoneProject'
MONGO_URI = os.environ.get('MONGO_URI')
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
recipes = mongo.db.recipes


@app.route('/')
@app.route('/browse_recipes')
def browse_recipes():
    return render_template('browse.html')


# form not iterating, can't cope with array in mongo, both ok, one not ok
@app.route('/search_recipes', methods=['POST', 'GET'])
def search_recipes():
    cuisine = request.form.getlist('cuisine')
    protein = request.form.getlist('protein')
    carbs = request.form.getlist('carbs')
    diet = request.form.getlist('diet')
    search = mongo.db.recipes.find({
                            'cuisine': {'$in': cuisine},
                            'protein': {'$in': protein},
                            'carbs': {'$in': carbs}, 'diet': {'$in': diet}
                            })
    print(cuisine, protein, carbs, diet)
    return render_template('search.html', recipes=search)


""" methods for browse page to sort by 1 thing
in browse.html and opens results.html """


@app.route('/search_italian', methods=['GET'])
def search_italian():
    italian = mongo.db.recipes.find({'cuisine': 'italian'})
    return render_template('results.html', recipes=italian)


@app.route('/search_rice', methods=['GET'])
def search_rice():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'carbs': 'rice'}))


@app.route('/search_vegetarian', methods=['GET'])
def search_vegetarian():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet': 'vegetarian'}))


@app.route('/search_pasta', methods=['GET'])
def search_pasta():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'carbs': 'pasta'}))


@app.route('/search_med', methods=['GET'])
def search_med():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine': 'mediterranean'}))


@app.route('/search_beef', methods=['GET'])
def search_beef():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein': 'beef'}))


@app.route('/search_poultry', methods=['GET'])
def search_poultry():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'protein': 'poultry'}))


@app.route('/search_lactose', methods=['GET'])
def search_lactose():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'diet': 'lactose free'}))


@app.route('/search_mexican', methods=['GET'])
def search_mexican():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                        {'cuisine': 'mexican'}))


@app.route('/search_pork', methods=['GET'])
def search_pork():
    return render_template('results.html', recipes=mongo.db.recipes.find(
                            {'protein': 'pork'}))


# add recipes

@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    recipes = mongo.db.recipes
    new_recipe = {
        'name': request.form.get('name'),
        'cuisine': request.form.getlist('cuisine'),
        'protein': request.form.getlist('protein'),
        'carbs': request.form.getlist('carbs'),
        'diet': request.form.getlist('diet'),
        'allergies': request.form.getlist('allergies'),
        'ingredients': request.form.getlist('ingredients'),
        'method': request.form.get('method'),
        'notes': request.form.get('notes')
        }
    recipes.insert_one(new_recipe)
    return render_template('add.html')

# update recipes


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('update.html', recipes=recipe)


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = mongo.db.recipes
    recipe.update({'_id': ObjectId(recipe_id)}, {
        'name': request.form.get('name'),
        'cuisine': request.form.getlist('cuisine'),
        'protein': request.form.getlist('protein'),
        'carbs': request.form.getlist('carbs'),
        'diet': request.form.getlist('diet'),
        'allergies': request.form.getlist('allergies'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'notes': request.form.get('notes')
        })

    return render_template('browse.html')


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return render_template('browse.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT'
            )), debug=True)
