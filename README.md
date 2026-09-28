# Sparta Cat
This is a song rating application project inspired by my UX Design course, for which we drafted the "look" of the app. And now, this serves as my attempt to implement it. 

## Dev Instruction
I cannot guarantee the correctness of these instructions. 
1. Tell me, and I will add you as collaborator
2. Install uv and FastAPI  
FastAPI is a backend framework, and uv is a package manager for python, like npm, in my understanding. Install both according to [https://fastapi.tiangolo.com/#installation](https://fastapi.tiangolo.com/#installation)
3. Clone this repo  
In your desired directory, run:   
`git clone https://github.com/896pw85v/my-sparta-cat.git`
4. Sync dependencies  
In the same directory, run:  
`uv sync`
5. (Optional) Install PostgreSQL  
This is optional because once I find a way to host the database there is no need for a local database. It's just that for now you can't test anything related to user and ratings. 

And now you can edit the project. Remember to make your own branch and merge after you made changes. 

To test the program, run `uv run fastapi dev`

## Current "System Design"
Backend is FastAPI which is also the frontend, providing frontend resources like html files and backend data. 
However, currently the backend serves only as a relay to the www.musicbrainz.org API, collecting data and send to users' browsers. User credential and song rating are now stored in PostgreSQL database, which in the future will be hosted on cloud. 

## Credits
The inspiration of this project: 
- https://github.com/Bishop-V
- https://github.com/Adrianne05
- Tejan
- https://github.com/JonIbarlin

Other: 
- Special thanks to https://musicbrainz.org/ for their dataset and API
- [PostgreSQL](https://www.postgresql.org/) is the best database in the world. 
- 李勃老师: https://space.bilibili.com/427191943