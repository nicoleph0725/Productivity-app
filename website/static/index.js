function deleteTask(taskId)  {
    fetch('/delete-task', {
        method:'POST',
        body:JSON.stringify({taskId: taskId}),
    }).then((_res) => {
        const taskElement = document.getElementById(`task-${taskId}`);
        // 2. Make it disappear from the screen
        if (taskElement) {
            taskElement.remove();
        }
    });
}

function toggleComplete(taskId) {
    fetch("/toggle-complete", {
        method: "POST",
        body: JSON.stringify({ taskId: taskId }),
        headers: {
            "Content-Type": "application/json",
        },
    }).then((res) => {
        if (res.ok) {
            // Find the task element in the HTML
            const taskElement = document.getElementById(`task-${taskId}`);

            const textElements = taskElement.querySelectorAll('h5, span');
            textElements.forEach(el => {
                el.classList.toggle('strikethrough');
                //el.classList.toggle('text-muted');
            });

        }
    });
}

//function toggleCompletedTasks() {
    //const completedTasksDiv = document.getElementById('completedTasksDiv');
    //const taskArrow = document.getElementById('taskArrow');
    //completedTasksDiv.classList.toggle('d-none');
    //taskArrow.classList.toggle('arrow-icon-rotated');
//}
function toggleCompletedTasks() {
    const taskDiv = document.getElementById('completedTasksDiv');
    const arrow = document.getElementById('taskArrow');

    // Toggle the 'd-none' class (Bootstrap's class for display: none)
    if (taskDiv.classList.contains('d-none')) {
        taskDiv.classList.remove('d-none'); // Show it
        arrow.style.transform = 'rotate(90deg)'; // Rotate arrow
    } else {
        taskDiv.classList.add('d-none'); // Hide it
        arrow.style.transform = 'rotate(0deg)'; // Reset arrow
    }
}