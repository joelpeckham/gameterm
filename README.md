# gameterm
Teaching computing concepts through a "gameified" command line.
This is an open source project by [Joel Peckham](https://www.instagram.com/joelskyler/) and Professor [Robert Ordóñez](http://computing.southern.edu/rordonez/) of [Southern Adventist University](https://www.southern.edu/).

Gameterm is a learning tool designed to teach basic computing concepts through a command-line interface. The tool allows instructors to create flexible (procedurally generated) exercises built around a command typed into either a BASH-like terminal or a Python REPL. These exercises come with prompts and hints, and also require the student to correctly type a command and get correct output. Prompts can be filled with narrative content, making the lesson feel more like a choose your own adventure game. Exercises can then be strung together into lessons and lessons can be made strung into courses. Both lessons and courses have internal mastery constraints requiring students to repeatedly get enough correct answers.

The front end (currently being built in Electron), has two main parts. The main part of the UI is a large terminal area where students can type commands. The second part of the UI is a sidebar where students can review the exercise requirements, view hints, and navigate the lesson.

The back end must manage progress tracking and mastery constraints and will ideally manage a sandbox filesystem for the student to work in.


# How to run locally

This whole project is an [Electron](https://electronjs.org/) app built on [node.js](https://nodejs.org/en/), so make sure you have [npm](https://www.npmjs.com/) installed.

First download and extract the project. (Or clone it see if I care.)

In a terminal, change directory to your clone like this:
```
cd ~/Downloads/gameterm-master
```
Then install dependencies with [npm](https://www.npmjs.com/):
```
npm install
```
Then, rerun electron-rebuild:
```
$(npm bin)/electron-rebuild
```
Or if you're on Windows:
```
.\node_modules\.bin\electron-rebuild.cmd
```
Start the application with [npm](https://www.npmjs.com/):
```
npm start
```
