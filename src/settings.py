from abc import ABC


class Settings(ABC):
    BASE_LEARNING_RATE = 0.001
    LEARNING_RATE_STEP = 0.001
    TENSORBOARD_PORT = 8051
    BASE_BATCH_SIZE = 1
