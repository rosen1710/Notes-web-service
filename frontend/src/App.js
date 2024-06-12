import React, { useState } from "react";
import './App.css';

import Keycloak from "keycloak-js";

const backendAddress = "localhost:5002";

let initOptions = {
  url: 'http://localhost:8080/',
  realm: 'notes-web-service',
  clientId: 'notes-web-service-client',
}

let kc = new Keycloak(initOptions);

kc.init({
  onLoad: 'login-required', // Supported values: 'check-sso' (default), 'login-required'
  checkLoginIframe: true
}).then((auth) => {
  if (!auth) {
    // window.location.reload();
  }
  else {
    console.log(kc.token)
  }
});

function App() {
  const [notes, setNotes] = useState([]);
  
  function fetchNotes() {
    fetch(`http://${backendAddress}/note/all`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to fetch notes');
      }
      return response.json();
    })
    .then(data => {
      setNotes(data.notes);
    })
    .catch(error => console.error('Error:', error));
  }
  
  function addNote() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const token = kc.token;
  
    fetch(`http://${backendAddress}/note`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title, description, token })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to add note');
      }
      return response.json();
    })
    .then(() => {
      fetchNotes();
      document.getElementById('announcementForm').reset();
    })
    .catch(error => console.error('Error:', error));
  }
  
  function editNote(id, oldTitle, oldDescription) {
    const newTitle = prompt('Enter new title:', oldTitle);
    const newDescription = prompt('Enter new description:', oldDescription);
  
    if (newTitle && newDescription) {
      fetch(`http://${backendAddress}/note/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: newTitle, description: newDescription, token: kc.token })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to edit note');
        }
        fetchNotes();
      })
      .catch(error => console.error('Error:', error));
    }
  }
  
  function deleteNote(id) {
    if (window.confirm('Are you sure you want to delete this note?')) {
      fetch(`http://${backendAddress}/note/${id}/${kc.token}`, {
        method: 'DELETE'
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to delete note');
        }
        fetchNotes();
      })
      .catch(error => console.error('Error:', error));
    }
  }

  if (notes.length === 0) {
    fetchNotes();
  }
  // setInterval(fetchNotes, 1000);

  return (
    <div>
      <h1>Announcement Notes</h1>

    {/* { aToken === null ? ( */}
      {/* <div style={{display: "flex", gap: "10px"}}>
        <button onClick={() => kc.login()}>Login</button>
        <button onClick={() => kc.register()}>Register</button>
        <button onClick={() => kc.logout()}>Logout</button>
      </div> */}
    {/* ) : ( */}
      <div>
        <button onClick={() => kc.logout()}>Logout from your account</button>
        <form id="announcementForm" onSubmit={(event) => {event.preventDefault();addNote();}}>
          <label for="title">Title:</label>
          <input type="text" id="title" required></input>
          <label for="description">Description:</label>
          <textarea id="description" required></textarea>
          <button type="submit">Add Note</button>
        </form>
      </div>
    {/* )} */}

      <div className="notes-container" id="notesContainer">
        { notes.map((note) => (
          <div>
            <h3>{note.title}</h3>
            <p>{note.description}</p>
            <p>Date & Time: {note.date_time.split("GMT")[0]}</p>
            { kc.tokenParsed.sub === note.user_id ? (
              <div>
                <button onClick={() => {editNote(note.id, note.title, note.description);}}>Edit</button>
                <button onClick={() => {deleteNote(note.id);}}>Delete</button>
                <br></br>
              </div>
            ) : (
              <div>
                <br></br>
                <br></br>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;