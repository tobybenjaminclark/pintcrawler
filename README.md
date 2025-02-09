Tavernstalk - A Pub Crawl Planner with a Twist
Inspiration
Britain has witnessed a somewhat partial demise of the humble boozer since the 1980s. Tavernstalk aims to get people out of the house, walking about, and socialising while revitalising this industry. In particular, we wanted to focus on the following points:

Planning a Pub Crawl is tricky! Especially when you don't know how safe the area is.
Leverage some classical computer science techniques to generate and rank 'crawls'.
Degrade a fun, sporadic social activity into a graph optimisation problem, then solve it.
Present all of this on a lovely website, and make it usable for the everyday taverngoer.
Make the optimisation function invertible (this is merely an instance of dark humor).
Something Different!
Tavernstalk offers the user a distinct choice instead of simply assuming the user wants to remain safe. Tweaking the parameters allows the algorithm to suggest dangerous routes, leading long walks through high crime areas to shady pubs and taverns - aptly named the Warriors Walk.

However (and more usefully) we also generate the safest pub crawls based on data obtained via the Police API (yes, this exists), named "The Peacekeeper's Path".

What it Does
Tavernstalk solves a parameterised routing problem to balance pub quality, walking distance between pubs, nearby crime rates, and presents this to quick-witted townsfolk in a medieval fashion:

User Input: The user enters a starting area and some of their preferences (such as rating of pubs, walking distance, and safety level).
Data Gathering: The algorithm pulls local pubs, routes from Google Maps, and crime data from the Police API (this is a real thing).
Route Calculation: The system calculates feasible routes, then uses some heuristics to filter down the search space.
Results: It presents the best pub crawl back to the user, with information about the pubs along the route and their safety ratings.
How We Built It & Challenges
This was our first time leveraging the traditional hacker weapon of React frontend and Flask backend – neither of which we are familiar with. This was an exciting learning experience, and we got to learn a lot, particularly about CORS, which was quite the hurdle.

We used Mapbox for presenting the geo-data, with NetworkX being used for mid-development backend workings.

Challenges
#1 Challenge: Devpost does not autosave, nor does it save when clicked (this is the third time I've written this 😤).
#2 Challenge: Handling multiple maps and managing state effectively.
#3 Challenge: Finding efficient routes within finite time constraints due to complex calculations.
Accomplishments We’re Proud Of & What We Learned!
Learning React and Flask: This project pushed us out of our comfort zone to learn a new stack, and it was incredibly rewarding.
Real-life Application: We were able to go on a pub crawl and see how the algorithm works in practice.
User Engagement: It's amazing to see people interacting with the site and enjoying the algorithm's recommendations.
Accuracy: Setting it up in our hometowns was a unique experience, and it was satisfying to see the algorithm accurately predict the best pubs and routes.
What’s Next for Tavernstalk?
Better User Experience: We aim to further improve the frontend with a more intuitive interface.
Enhanced Data: We hope to integrate more detailed pub data and expand crime data for even more accurate recommendations.
Additional Features: Possible future features include adding the option to customize routes based on drink preferences, weather conditions, or even event-based crawling.
