import click
from sqlalchemy.orm import Session
from contextlib import closing
from models.database import SessionLocal
from models.user import User
from models.destination import Destination
from models.trip import Trip

@click.group()
def cli():
    """Travel Planner CLI"""
    pass

# Command to create a new user
@cli.command()
@click.option('--name', prompt='Your name', help="The user's name")
@click.option('--email', prompt='Your email', help="The user's email")
def create_user(name, email):
    """Create a new user"""
    try:
        with closing(SessionLocal()) as session:
            new_user = User(name=name, email=email)
            session.add(new_user)
            session.commit()
            click.echo(f'User {name} created successfully!')
    except Exception as e:
        click.echo(f'Error creating user: {e}')

# Command to list all available destinations
@cli.command()
def list_destinations():
    """List all available destinations"""
    try:
        with closing(SessionLocal()) as session:
            destinations = session.query(Destination).all()
            for destination in destinations:
                click.echo(f'{destination.id}: {destination.name} - {destination.description}')
    except Exception as e:
        click.echo(f'Error retrieving destinations: {e}')

# Command to book a trip
@cli.command()
@click.option('--user_id', prompt='User ID', help="ID of the user")
@click.option('--destination_id', prompt='Destination ID', help="ID of the destination")
def book_trip(user_id, destination_id):
    """Book a trip for a user"""
    try:
        with closing(SessionLocal()) as session:
            user = session.query(User).get(user_id)
            destination = session.query(Destination).get(destination_id)

            if not user:
                click.echo('User not found.')
                return
            if not destination:
                click.echo('Destination not found.')
                return

            new_trip = Trip(user_id=user.id, destination_id=destination.id)
            session.add(new_trip)
            session.commit()
            click.echo(f'Trip booked for {user.name} to {destination.name}! Trip ID: {new_trip.id}')
    except Exception as e:
        click.echo(f'Error booking trip: {e}')

# Command to view all trips for a user
@cli.command()
@click.option('--user_id', prompt='User ID', help="ID of the user")
def view_trips(user_id):
    """View all trips booked by a user"""
    try:
        with closing(SessionLocal()) as session:
            user = session.query(User).get(user_id)

            if not user:
                click.echo('User not found.')
                return

            trips = session.query(Trip).filter(Trip.user_id == user.id).all()
            if trips:
                click.echo(f'{user.name} has booked the following trips:')
                for trip in trips:
                    destination = session.query(Destination).get(trip.destination_id)
                    click.echo(f'- {destination.name} (Trip ID: {trip.id})')
            else:
                click.echo(f'{user.name} has no trips booked.')
    except Exception as e:
        click.echo(f'Error retrieving trips: {e}')

# Command to list all users
@cli.command()
def list_users():
    """List all users"""
    try:
        with closing(SessionLocal()) as session:
            users = session.query(User).all()
            for user in users:
                click.echo(f'{user.id}: {user.name} - {user.email}')
    except Exception as e:
        click.echo(f'Error retrieving users: {e}')

if __name__ == "__main__":
    cli()

