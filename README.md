# AminoScore

Repo to manage backend and frontend(s) for a recommendation system to help users with plant based nutrition. The main focus is on combining foods in a way, that the contained essential amino acids add to full human usable proteins (boost the biological value by smart combinations).

Backend
-------

The first goal is to build a backend sending a hand full of complementing foods to a request containing a hand full of selected foods and the amino acid compositions of the requested and calculated complementary foods.

Frontend
--------

The first increment will provide an easy- to- use and nice web UI being able to perform the following tasks:

- input a selection of foods to which complementary ones should be calculated by the backend
- visualize the result as stacked bar graph
- calculate the biologial value ("Amino Score") of the current combination and visualize it
- wipe off unwanted foods and send a replacement request to the backend
- visually blend the recommended foods by a "console" 
- output the result in realtime in the stacked bar graph and the overall "Amino Score" 
