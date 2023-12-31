from typing import Union

import torch.nn as nn
from omegaconf import DictConfig

from src.models.decoder.lstmdecoder import LSTMDecoder
from src.models.decoder.mlpdecoder import MLPDecoder
from src.models.decoder.transformerdecoder import TransformerDecoder
from src.models.decoder.transformerdecoderx import TransformerDecoderx
from src.models.decoder.unet1ddecoder import UNet1DDecoder
from src.models.decoder.unet1ddecoderlstm import UNet1DDecoderLSTM
from src.models.decoder.unet1ddecodrtransformer import UNet1DDecoderTransformer
from src.models.feature_extractor.cnn import CNNSpectrogram
from src.models.feature_extractor.cnn_wave import WaveNetSpectrogram
from src.models.feature_extractor.lstm import LSTMFeatureExtractor
from src.models.feature_extractor.panns import PANNsFeatureExtractor
from src.models.feature_extractor.resid_gru import ResidGRUFeatureExtractor
from src.models.feature_extractor.spectrogram import SpecFeatureExtractor
from src.models.feature_extractor.wavelstm import LSTMWaveNetSpectrogram
from src.models.spec1D import Spec1D
from src.models.spec2Dcnn import Spec2DCNN

FEATURE_EXTRACTORS = Union[
    CNNSpectrogram,
    PANNsFeatureExtractor,
    LSTMFeatureExtractor,
    SpecFeatureExtractor,
    WaveNetSpectrogram,
    ResidGRUFeatureExtractor,
    LSTMWaveNetSpectrogram,
]
DECODERS = Union[UNet1DDecoder, LSTMDecoder, TransformerDecoder, MLPDecoder, UNet1DDecoderLSTM]
MODELS = Union[Spec1D, Spec2DCNN]


def get_feature_extractor(
    cfg: DictConfig, feature_dim: int, num_timesteps: int
) -> FEATURE_EXTRACTORS:
    feature_extractor: FEATURE_EXTRACTORS
    if cfg.feature_extractor.name == "CNNSpectrogram":
        feature_extractor = CNNSpectrogram(
            in_channels=feature_dim,
            base_filters=cfg.feature_extractor.base_filters,
            kernel_sizes=cfg.feature_extractor.kernel_sizes,
            stride=cfg.feature_extractor.stride,
            sigmoid=cfg.feature_extractor.sigmoid,
            output_size=num_timesteps,
            conv=nn.Conv1d,
            reinit=cfg.feature_extractor.reinit,
        )
    elif cfg.feature_extractor.name == "WaveNetSpectrogram":
        feature_extractor = WaveNetSpectrogram(
            in_channels=feature_dim,
            base_filters=cfg.feature_extractor.base_filters,
            wave_layers=cfg.feature_extractor.wave_layers,
            wave_block=cfg.feature_extractor.wave_block,
            kernel_size=cfg.feature_extractor.kernel_size,
            downsample=cfg.feature_extractor.downsample,
            sigmoid=cfg.feature_extractor.sigmoid,
            output_size=num_timesteps,
            reinit=cfg.feature_extractor.reinit,
        )
    elif cfg.feature_extractor.name == "LSTMWaveNetSpectrogram":
        feature_extractor = LSTMWaveNetSpectrogram(
            in_channels=feature_dim,
            base_filters=cfg.feature_extractor.base_filters,
            wave_layers=cfg.feature_extractor.wave_layers,
            wave_block=cfg.feature_extractor.wave_block,
            kernel_size=cfg.feature_extractor.kernel_size,
            downsample=cfg.feature_extractor.downsample,
            sigmoid=cfg.feature_extractor.sigmoid,
            output_size=num_timesteps,
            reinit=cfg.feature_extractor.reinit,
        )
    elif cfg.feature_extractor.name == "PANNsFeatureExtractor":
        feature_extractor = PANNsFeatureExtractor(
            in_channels=feature_dim,
            base_filters=cfg.feature_extractor.base_filters,
            kernel_sizes=cfg.feature_extractor.kernel_sizes,
            stride=cfg.feature_extractor.stride,
            sigmoid=cfg.feature_extractor.sigmoid,
            output_size=num_timesteps,
            conv=nn.Conv1d,
            reinit=cfg.feature_extractor.reinit,
            win_length=cfg.feature_extractor.win_length,
        )
    elif cfg.feature_extractor.name == "LSTMFeatureExtractor":
        feature_extractor = LSTMFeatureExtractor(
            in_channels=feature_dim,
            hidden_size=cfg.feature_extractor.hidden_size,
            num_layers=cfg.feature_extractor.num_layers,
            bidirectional=cfg.feature_extractor.bidirectional,
            out_size=num_timesteps,
        )
    elif cfg.feature_extractor.name == "ResidGRUFeatureExtractor":
        feature_extractor = ResidGRUFeatureExtractor(
            in_channels=feature_dim,
            hidden_size=cfg.feature_extractor.hidden_size,
            num_layers=cfg.feature_extractor.num_layers,
            bidirectional=cfg.feature_extractor.bidirectional,
            out_size=num_timesteps,
        )
    elif cfg.feature_extractor.name == "SpecFeatureExtractor":
        feature_extractor = SpecFeatureExtractor(
            in_channels=feature_dim,
            height=cfg.feature_extractor.height,
            hop_length=cfg.feature_extractor.hop_length,
            win_length=cfg.feature_extractor.win_length,
            out_size=num_timesteps,
        )
    else:
        raise ValueError(f"Invalid feature extractor name: {cfg.feature_extractor.name}")

    return feature_extractor


def get_decoder(cfg: DictConfig, n_channels: int, n_classes: int, num_timesteps: int) -> DECODERS:
    decoder: DECODERS
    if cfg.decoder.name == "UNet1DDecoder":
        decoder = UNet1DDecoder(
            n_channels=n_channels,
            n_classes=n_classes,
            duration=num_timesteps,
            bilinear=cfg.decoder.bilinear,
            se=cfg.decoder.se,
            res=cfg.decoder.res,
            scale_factor=cfg.decoder.scale_factor,
            dropout=cfg.decoder.dropout,
        )
    elif cfg.decoder.name == "UNet1DDecoderLSTM":
        decoder = UNet1DDecoderLSTM(
            n_channels=n_channels,
            n_classes=n_classes,
            duration=num_timesteps,
            bilinear=cfg.decoder.bilinear,
            se=cfg.decoder.se,
            res=cfg.decoder.res,
            scale_factor=cfg.decoder.scale_factor,
            dropout=cfg.decoder.dropout,
            num_layers=cfg.decoder.num_layers,
        )
    elif cfg.decoder.name == "UNet1DDecoderTransformer":
        decoder = UNet1DDecoderTransformer(
            n_channels=n_channels,
            n_classes=n_classes,
            duration=num_timesteps,
            bilinear=cfg.decoder.bilinear,
            se=cfg.decoder.se,
            res=cfg.decoder.res,
            scale_factor=cfg.decoder.scale_factor,
            dropout=cfg.decoder.dropout,
            num_layers=cfg.decoder.num_layers,
        )
    elif cfg.decoder.name == "LSTMDecoder":
        decoder = LSTMDecoder(
            input_size=n_channels,
            hidden_size=cfg.decoder.hidden_size,
            num_layers=cfg.decoder.num_layers,
            dropout=cfg.decoder.dropout,
            bidirectional=cfg.decoder.bidirectional,
            n_classes=n_classes,
        )
    elif cfg.decoder.name == "TransformerDecoder":
        decoder = TransformerDecoder(
            input_size=n_channels,
            hidden_size=cfg.decoder.hidden_size,
            num_layers=cfg.decoder.num_layers,
            dropout=cfg.decoder.dropout,
            nhead=cfg.decoder.nhead,
            n_classes=n_classes,
        )
    elif cfg.decoder.name == "TransformerDecoderx":
        decoder = TransformerDecoderx(
            input_size=n_channels,
            hidden_size=cfg.decoder.hidden_size,
            num_layers=cfg.decoder.num_layers,
            dropout=cfg.decoder.dropout,
            nhead=cfg.decoder.nhead,
            n_classes=n_classes,
        )
    elif cfg.decoder.name == "MLPDecoder":
        decoder = MLPDecoder(n_channels=n_channels, n_classes=n_classes)
    else:
        raise ValueError(f"Invalid decoder name: {cfg.decoder.name}")

    return decoder


def get_model(cfg: DictConfig, feature_dim: int, n_classes: int, num_timesteps: int) -> MODELS:
    model: MODELS
    if cfg.model.name == "Spec2DCNN":
        feature_extractor = get_feature_extractor(cfg, feature_dim, num_timesteps)
        decoder = get_decoder(cfg, feature_extractor.height, n_classes, num_timesteps)
        model = Spec2DCNN(
            feature_extractor=feature_extractor,
            decoder=decoder,
            encoder_name=cfg.model.encoder_name,
            in_channels=feature_extractor.out_chans,
            encoder_weights=cfg.model.encoder_weights,
            mixup_alpha=cfg.augmentation.mixup_alpha,
            cutmix_alpha=cfg.augmentation.cutmix_alpha,
        )
    elif cfg.model.name == "Spec1D":
        feature_extractor = get_feature_extractor(cfg, feature_dim, num_timesteps)
        decoder = get_decoder(cfg, feature_extractor.height, n_classes, num_timesteps)
        model = Spec1D(
            feature_extractor=feature_extractor,
            decoder=decoder,
            mixup_alpha=cfg.augmentation.mixup_alpha,
            cutmix_alpha=cfg.augmentation.cutmix_alpha,
        )
    else:
        raise NotImplementedError

    return model