# todo/views.py

from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password


from django.urls import reverse

from .models import TodoTask

from django.contrib import messages  # Import messages



from django.shortcuts import render, redirect, get_object_or_404

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Hash the password before saving
        hashed_password = make_password(password)
        
        # Create and save the user
        user = CustomUser(username=username, email=email, password=hashed_password)
        user.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user exists
        user = CustomUser.objects.filter(username=username).first()
        
        if user:
            # Verify the password
            if check_password(password, user.password):
                # Login successful, retrieve user_id
                user_id = user.id
                # Redirect to todo_dashboard with user_id
                return redirect('todo_dashboard', user_id=user_id)
        
        # Login failed, redirect back to login page
        return redirect('login')
    else:
        return render(request, 'login.html')




def logout_view(request):
    # Implement logout functionality here
    return redirect('login')




def todo_dashboard(request, user_id):  # Modify the view to accept user_id parameter
    print("the useris iddddd: ", user_id)

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        due_date = request.POST.get('due_date')
        status = 'Pending'  # Assuming newly added tasks are initially pending

        # Create the TodoTask object with the user ID
        TodoTask.objects.create(
            user_id=user_id,
            task_name=task_name,
            due_date=due_date,
            status=status
        )

        # Optionally, you can add a success message
        messages.success(request, 'Task added successfully.')

        # Redirect to the same page to prevent form resubmission
        return redirect('todo_dashboard', user_id=user_id)

    # Determine which tasks to display based on the query parameter 'status'
    status = request.GET.get('status', 'pending')

    if status == 'completed':
        tasks = TodoTask.objects.filter(user_id=user_id, status='Completed')
    elif status == 'expired':
        tasks = TodoTask.objects.filter(user_id=user_id, status='Expired')
    else:  # Default to pending tasks
        tasks = TodoTask.objects.filter(user_id=user_id, status='Pending')

    # Render the todo dashboard template with the tasks
    return render(request, 'todo_dashboard.html', {
        'tasks': tasks,
        'status': status.capitalize(),
        'user_id': user_id,  # Pass the user_id to the template
    })




def mark_completed(request, task_id):
    task = get_object_or_404(TodoTask, id=task_id)
    task.status = 'Completed'
    task.save()
    # Retrieve the user_id from the task object
    user_id = task.user_id
    # Redirect to todo_dashboard with user_id
    return redirect('todo_dashboard', user_id=user_id)




def delete_task(request, task_id):
    # Retrieve the task object or return a 404 error if it doesn't exist
    task = get_object_or_404(TodoTask, id=task_id)
    # Retrieve the user_id from the task object
    user_id = task.user_id
    # Delete the task
    task.delete()
    # Optionally, add a success message
    messages.success(request, 'Task deleted successfully.')
    # Redirect to the todo dashboard or any other appropriate page
    return redirect('todo_dashboard', user_id=user_id)




def edit_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(TodoTask, id=task_id)
        task.task_name = request.POST.get('task_name')
        task.due_date = request.POST.get('due_date')
        task.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('todo_dashboard')
    else:
        task = get_object_or_404(TodoTask, id=task_id)
        return render(request, 'edit_task.html', {'task': task})






#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx