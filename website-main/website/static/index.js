// function deleteNote(noteId) {
//   fetch("/delete-note", {
//     method: "POST",
//     body: JSON.stringify({ noteId: noteId }),
//   }).then((_res) => {
//     window.location.href = "/";
//   });
// }

function deleteAvailability(availabilityId) {
    fetch("/delete-availability", {
      method: "POST",
      body: JSON.stringify({ availabilityId: availabilityId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

// function deleteUser(userId) {
//   fetch(`/delete-user/${userId}`, {
//     method: "POST",
//     body: JSON.stringify({ userId: userId }),
//   })
//     .then((_res) => {
//       // Assuming you want to redirect to a page after successful deletion
//       window.location.href = "/";
//     })
//     .catch((error) => {
//       // Handle any errors that occur during the fetch request
//       console.error("Error deleting user:", error);
//     });
// }
