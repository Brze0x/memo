from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def main():
    card = Memo()
    card.select_actions()
    

class MemoDB(Base):
    __tablename__ = 'memo'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


class Memo:
    def __init__(self):
        engine = create_engine('sqlite:///data/flashcard.db?check_same_thread=False')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_card(self):
        action = input("\n1. Add a new flashcard\n2. Exit\n").strip()
        while action != '2':
            if action == '1':
                term = input("\nQuestion:\n").strip()
                while not term:
                    term = input("Question:\n").strip()
                definition = input("Answer:\n").strip()
                while not definition:
                    definition = input("Answer:\n").strip()
                new_data = MemoDB(question=term, answer=definition, box=1)
                self.session.add(new_data)
                self.session.commit()

            if action not in ['1', '2']:
                print(f"\n{action} is not an option")

            action = input("\n1. Add a new flashcard\n2. Exit\n").strip()
        print()

    def practice_cards(self):
        result_list = self.session.query(MemoDB).all()
        for idx in range(len(result_list)):
            print(f"\nQuestion: {result_list[idx].question}")
            answer = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n').strip()
            while answer not in ['y', 'n', 'u']:
                print(f"{answer} is not an option")
                answer = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n').strip()
            if answer == 'y':
                print(f"\nAnswer: {result_list[idx].answer}")
                choice = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n').strip()
                while choice not in ['y', 'n']:
                    print(f"{choice} is not an option")
                    choice = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n').strip()
                if choice == 'y':
                    if result_list[idx].box == 3:
                        self.session.delete(result_list[idx])
                    else:
                        result_list[idx].box = result_list[idx].box + 1
                    self.session.commit()
                elif choice == 'n':
                    if result_list[idx].box == 1:
                        result_list[idx].box = result_list[idx].box
                    else:
                        result_list[idx].box = result_list[idx].box - 1
                    self.session.commit()
            elif answer == 'u':
                update = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n').strip()
                while update not in ['d', 'e']:
                    print(f"{update} is not an option")
                    update = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n').strip()
                
                if update == 'd':
                    self.delete_card(result_list=result_list, idx=idx)
                elif update == 'e':
                    self.update_card(result_list=result_list, idx=idx)  
            elif answer == 'n':
                continue
        print()
    
    def delete_card(self, result_list: list, idx: int):
        self.session.delete(result_list[idx])
        self.session.commit()

    def update_card(self, result_list: list, idx: int):
        print(f"\ncurrent question: {result_list[idx].question}")
        term = input("please write a new question:\n").strip()
        if term == '':
            term = result_list[idx].question
        else:
            term = term
        self.session.query(MemoDB).filter(MemoDB.id == idx + 1).update({MemoDB.question: term})
        self.session.commit()
        print(f"current answer: {result_list[idx].answer}")
        definition = input("please write a new answer:\n").strip()
        if definition == '':
            definition = result_list[idx].answer
        else:
            definition = definition
        self.session.query(MemoDB).filter(MemoDB.id == idx + 1).update({MemoDB.answer: definition})
        self.session.commit()

    def select_actions(self):
        action = input("1. Add flashcards\n2. Practice flashcards\n3. Exit\n").strip()
        while action != '3':
            if action == '1':
                self.add_card()
            if action == '2':
                if len(self.session.query(MemoDB).all()) != 0:
                    self.practice_cards()
                else:
                    print("There is no flashcard to practice!\n")
            if action not in ['1', '2', '3']:
                print(f"\n{action} is not an option")
    
            action = input("1. Add flashcards\n2. Practice flashcards\n3. Exit\n").strip()
        print("\nBye!")

if __name__ == '__main__':
    main()
