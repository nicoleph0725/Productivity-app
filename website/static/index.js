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
