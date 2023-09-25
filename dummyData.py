from app import db, ConstitutionalConvention, Committees, Debates, Documents, Commentaries,app
from datetime import datetime  # Import datetime module for date parsing

from app import db

def create_dummy_data():
    with app.app_context():  # Establish the Flask application context

        # Create Constitutional Convention data
        convention1 = ConstitutionalConvention(
            date=datetime(1776, 7, 4),
            location="Philadelphia",
            participants="Thomas Jefferson, John Adams, Benjamin Franklin",
        )
        convention1.create()

        convention2 = ConstitutionalConvention(
            date=datetime(1787, 5, 25),
            location="Philadelphia",
            participants="George Washington, James Madison, Alexander Hamilton",
        )
        convention2.create()

        # Create Committee data
        committee1 = Committees(
            committee_name="Declaration Committee",
            committee_members="Thomas Jefferson, John Adams, Benjamin Franklin",
            topics_covered="Drafting the Declaration of Independence",
        )
        committee1.create()

        committee2 = Committees(
            committee_name="Constitution Committee",
            committee_members="George Washington, James Madison, Alexander Hamilton",
            topics_covered="Drafting the U.S. Constitution",
        )
        committee2.create()

        # Create Document data
        document1 = Documents(
            document_type="Declaration of Independence",
            author="Thomas Jefferson",
            document_content="We hold these truths to be self-evident...",
        )
        document1.create()

        document2 = Documents(
            document_type="U.S. Constitution",
            author="James Madison",
            document_content="We the People of the United States...",
        )
        document2.create()

        # Create Debate data
        debate1 = Debates(
            debate_date=datetime(1776, 7, 2),
            debate_location="Philadelphia",
            participants="Participants A, Participants B",
            debate_content="Debate content 1",
            committee_id=committee1.committee_id,
            document_id=document1.document_id,
        )
        debate1.create()

        debate2 = Debates(
            debate_date=datetime(1787, 5, 23),
            debate_location="Philadelphia",
            participants="Participants C, Participants D",
            debate_content="Debate content 2",
            committee_id=committee2.committee_id,
            document_id=document2.document_id,
        )
        debate2.create()

        # Create Commentary data
        commentary1 = Commentaries(
            author="John Adams",
            timestamp=datetime(1776, 7, 4),
            commentary_text="Great document!",
            debate_id=debate1.debate_id,
            document_id=document1.document_id,
        )
        commentary1.create()

        commentary2 = Commentaries(
            author="Alexander Hamilton",
            timestamp=datetime(1787, 5, 25),
            commentary_text="Exciting times!",
            debate_id=debate2.debate_id,
            document_id=document2.document_id,
        )
        commentary2.create()

if __name__ == "__main__":
    create_dummy_data()