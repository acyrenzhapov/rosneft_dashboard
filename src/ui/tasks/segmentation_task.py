from tensorboard.program import TensorBoard

from src.network.unet3d.unet3d256 import UNet3D_256
from src.settings import Settings
from src.network.train import LitModel
import segmentation_models_pytorch as smp
import pytorch_lightning as pl
from src.network.dataset import SegyDataset
from torch.utils.data import DataLoader
from pytorch_lightning.loggers import TensorBoardLogger


class SegmentationTask(object):
    """Pipeline to train model."""
    def __init__(self):
        self._tensorboard = None
        self._pl_tensorboard = TensorBoardLogger(
            '/logs/',
            name='fault_detection_v1'
        )

    def launch(self):
        """Start pipeline to train model."""
        self._tensorboard = TensorBoard()
        self._tensorboard.configure(
            argv=[  # noqa:WPS317
                None,
                '--logdir', str('/lightning_logs/'),
                '--port', str(Settings.TENSORBOARD_PORT),
            ],
        )
        self._tensorboard.launch()

    def train(
        self,
        model_type: str,
        model_path: str,
        lr_value: float,
        epoch_size: int,
        batch_size: int,
        device_type: str,
        seis_path: str,
        fault_mask_path: str,
        coords_mask_path: str,
    ):
        train_dataset = SegyDataset(
            segy_filepath=seis_path,
            fault_filepath=fault_mask_path,
            fault_coords_filepath=coords_mask_path,
        )
        eval_dataset = SegyDataset(
            segy_filepath=seis_path,
            fault_filepath=fault_mask_path,
            fault_coords_filepath='..\\..\\data\\mask_test.txt'
        )
        trainloader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            num_workers=8,
        )
        evalloader = DataLoader(
            eval_dataset,
            batch_size=batch_size,
            num_workers=8,
        )
        model = UNet3D_256()
        tversky_loss = smp.losses.TverskyLoss(
            mode='binary',
            beta=0.3,
        )
        device = 'cpu'
        print(device_type)
        if device_type == 'Видеокарта':
            device = 'gpu'
        lit_model = LitModel(
            model=model,
            loss=tversky_loss,
            lr_rate=lr_value,
        )
        print(device)
        trainer_model = pl.Trainer(
            max_epochs=epoch_size,
            accelerator=device,
            # logger=self._pl_tensorboard
        )
        print('start training')
        trainer_model.fit(lit_model, trainloader, evalloader)
        print('training end')
