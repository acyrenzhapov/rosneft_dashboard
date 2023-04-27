import pytorch_lightning as pl
from torch import optim


class LitModel(pl.LightningModule):
    def __init__(
        self,
        model,
        loss,
        lr_rate: float,
    ):
        super().__init__()
        self._lr_rate = lr_rate
        self.model = model
        self.loss = loss
        self.valid_loss = []
        self.train_loss = []

    def forward(self, x):
        y_pred = self.model(x)
        return y_pred

    def configure_optimizers(self):
        optimizer = optim.Adam(self.model.parameters(), lr=self._lr_rate)
        return optimizer

    def get_metrics(self, y_pred, y, metrics_type="train"):
        return 0
        # values = smp.metrics.functional.get_stats(
        #     (y_pred > 0.5).type(torch.int32), y.type(torch.int32),
        #     mode='binary'
        #     )
        # iou = smp.metrics.functional.iou_score(*values)
        # self.log(f'iou/{metrics_type}', torch.mean(iou))

    def training_step(self, batch, batch_idx):
        x, y = batch

        y_pred = self.forward(x)
        loss = self.loss(y_pred, y)
        correct = y_pred.argmax(dim=1).eq(y).sum().item()
        self.train_loss.append(loss)
        # self.get_metrics(y_pred, y, 'train')
        logs = {"train_loss": loss}
        return loss
        return {
            'loss': loss,
            'log': logs,
            'correct': correct,
            'total': len(y)
        }

    def validation_step(self, val_batch, batch_idx):
        x, y = val_batch

        y_pred = self.forward(x)
        loss = self.loss(y_pred, y)
        correct = y_pred.argmax(dim=1).eq(y).sum().item()
        self.valid_loss.append(loss)
        # self.get_metrics(y_pred, y, 'valid')
        logs = {"train_loss": loss}
        return loss
        return {
            'loss': loss,
            'log': logs,
            'correct': correct,
            'total': len(y)
        }

    def test_step(self, batch, batch_idx):
        x, y = batch

        y_pred = self.forward(x)
        loss = self.loss(y_pred, y)
        # self.get_metrics(y_pred, y, 'test')
        return loss
