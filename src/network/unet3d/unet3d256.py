import torch
from torch import nn


class UNet3D_256(nn.Module):
    def __init__(self):
        super(UNet3D_256, self).__init__()

        self.layer_encoder_1 = self.__get_encoder_layer(
            1, 16, kernel_size=3, stride=1, padding=1
            )
        self.layer_encoder_2 = self.__get_encoder_layer(
            16, 32, kernel_size=3, stride=1, padding=1
            )

        self.layer_encoder_3 = self.__get_encoder_layer(
            32, 32, kernel_size=3, stride=1, padding=1
            )
        self.layer_encoder_4 = self.__get_encoder_layer(
            32, 64, kernel_size=3, stride=1, padding=1
            )

        self.layer_encoder_5 = self.__get_encoder_layer(
            64, 64, kernel_size=3, stride=1, padding=1
            )
        self.layer_encoder_6 = self.__get_encoder_layer(
            64, 128, kernel_size=3, stride=1, padding=1
            )

        self.layer_encoder_7 = self.__get_encoder_layer(
            128, 128, kernel_size=3, stride=1, padding=1
            )
        self.layer_encoder_8 = self.__get_encoder_layer(
            128, 256, kernel_size=3, stride=1, padding=1
            )

        self.max_pool_1 = nn.MaxPool3d(2)
        self.max_pool_2 = nn.MaxPool3d(2)
        self.max_pool_3 = nn.MaxPool3d(2)

        self.layer_decoder_1 = self.__get_decoder_layer(
            256, 256, kernel_size=2, stride=2
            )
        self.layer_decoder_2 = self.__get_encoder_layer(
            128 + 256, 128, kernel_size=3, stride=1, padding=1
            )
        self.layer_decoder_3 = self.__get_encoder_layer(
            128, 128, kernel_size=3, stride=1, padding=1
            )

        self.layer_decoder_4 = self.__get_decoder_layer(
            128, 128, kernel_size=2, stride=2
            )
        self.layer_decoder_5 = self.__get_encoder_layer(
            64 + 128, 64, kernel_size=3, stride=1, padding=1
            )
        self.layer_decoder_6 = self.__get_encoder_layer(
            64, 64, kernel_size=3, stride=1, padding=1
            )

        self.layer_decoder_7 = self.__get_decoder_layer(
            64, 64, kernel_size=2, stride=2
            )
        self.layer_decoder_8 = self.__get_encoder_layer(
            32 + 64, 32, kernel_size=3, stride=1, padding=1
            )
        self.layer_decoder_9 = self.__get_encoder_layer(
            32, 1, kernel_size=3, stride=1, padding=1
            )
        self.layer_10 = nn.Sequential(nn.Conv3d(1, 1, kernel_size=1, stride=1))
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # ----------encoder start----------

        first_layer_encoder = self.layer_encoder_2(self.layer_encoder_1(x))
        x = self.max_pool_1(first_layer_encoder)

        second_layer_encoder = self.layer_encoder_4(self.layer_encoder_3(x))
        x = self.max_pool_2(second_layer_encoder)
        third_layer_encoder = self.layer_encoder_6(self.layer_encoder_5(x))

        x = self.max_pool_3(third_layer_encoder)
        x = self.layer_encoder_8(self.layer_encoder_7(x))
        # ----------encoder end----------

        # ----------decoder start----------
        x = self.layer_decoder_1(x)
        third_layer_decoder = torch.cat((x, third_layer_encoder), 1)
        del third_layer_encoder
        x = self.layer_decoder_3(self.layer_decoder_2(third_layer_decoder))
        del third_layer_decoder

        x = self.layer_decoder_4(x)
        second_layer_decoder = torch.cat((x, second_layer_encoder), 1)
        del second_layer_encoder
        x = self.layer_decoder_6(self.layer_decoder_5(second_layer_decoder))
        del second_layer_decoder

        x = self.layer_decoder_7(x)
        first_layer_decoder = torch.cat((x, first_layer_encoder), 1)
        del first_layer_encoder
        x = self.layer_decoder_9(self.layer_decoder_8(first_layer_decoder))
        del first_layer_decoder
        # ----------edcoder end----------
        x = self.layer_10(x)
        # x = self.sigmoid(x)
        return x

    def __get_encoder_layer(
        self, input_channel=1, output_channel=64, kernel_size=3, stride=1,
        padding=0, batch_norm=True, padding_mode='replicate'
        ):
        if batch_norm:
            return nn.Sequential(
                nn.Conv3d(
                    input_channel, output_channel,
                    kernel_size=kernel_size, stride=stride, padding=padding,
                    padding_mode=padding_mode
                    ),
                nn.BatchNorm3d(output_channel),
                nn.ReLU()
                )
        return nn.Sequential(
            nn.Conv3d(
                input_channel, output_channel, kernel_size=kernel_size,
                stride=stride, padding=padding
                ),
            nn.ReLU()
            )

    def __get_decoder_layer(
        self, input_channel=1, output_channel=64, kernel_size=3, stride=1,
        padding=0
        ):
        return nn.Sequential(
            nn.ConvTranspose3d(
                input_channel, output_channel, kernel_size=kernel_size,
                stride=stride, padding=padding
                )
            )