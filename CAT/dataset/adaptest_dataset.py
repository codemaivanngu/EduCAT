from collections import defaultdict, deque
import torch

try:
    # for python module
    from .dataset import Dataset
    from .train_dataset import TrainDataset
except (ImportError, SystemError):  # pragma: no cover
    # for python script
    from dataset import Dataset
    from train_dataset import TrainDataset


class AdapTestDataset(Dataset):

    def __init__(self, data, concept_map,
                 num_students, num_questions, num_concepts):
        """
        Args:
            data: list, [(sid, qid, score)]
            concept_map: dict, concept map {qid: cid}
            num_students: int, total student number
            num_questions: int, total question number
            num_concepts: int, total concept number
        """
        super().__init__(data, concept_map,
                         num_students, num_questions, num_concepts)

        # initialize tested and untested set
        self.tested = None
        self.untested = None
        self.reset()

    def apply_selection(self, student_idx, question_idx):
        """ 
        Add one untested question to the tested set
        Args:
            student_idx: int
            question_idx: int
        """
        assert question_idx in self.untested[student_idx], \
            'Selected question not allowed'
        self.untested[student_idx].remove(question_idx)
        self.tested[student_idx].append(question_idx)

    def reset(self):
        """ 
        Set tested set empty
        """
        self.tested = defaultdict(deque)
        self.untested = defaultdict(set)
        for sid in self.data:
            self.untested[sid] = set(self.data[sid].keys())

    @property
    def tested(self):
        return self.tested

    @property
    def untested(self):
        return self.untested

    def get_tested_dataset(self, last=False):
        """
        Get tested data for training
        Args: 
            last: bool, True - the last question, False - all the tested questions
        Returns:
            TrainDataset
        """
        triplets = []
        for sid, qids in self.tested.items():
            if last:
                qid = qids[-1]
                triplets.append((sid, qid, self.data[sid][qid]))
            else:
                for qid in qids:
                    triplets.append((sid, qid, self.data[sid][qid]))
        return TrainDataset(triplets, self.concept_map,
                            self.num_students, self.num_questions, self.num_concepts)