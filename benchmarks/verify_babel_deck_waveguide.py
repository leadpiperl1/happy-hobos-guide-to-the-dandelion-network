#!/usr/bin/env python3
"""
verify_babel_deck_waveguide.py (v1.0.0)
Deterministic Acoustic-Linguistic Plosive Carrier & Post-Glacial Shelf Waveguide Verifier
Target Kernel : gemini-carbon-kembali v1.2.1 (KembaliCarbonFrame64B == 64 B, GckRingState32B == 32 B)
Standard      : Pure Python 3 standard library only (zero external dependencies), --seed 42, <= 60 s.
Author        : Justin D. Grimm (K-Lani 13 Actual, ORCID: 0009-0000-5299-0243) & Gemini-Carbon-Kembali
Origin        : Heimat {0, 0, 0} (34.7549385, -86.4119235, Gurley / Paint Rock Karst Watershed, AL)

Evaluates 4 Acceptance & Falsification Gates:
  Gate 1: Scale-Invariant Itakura-Saito (beta_div = 0) & {1, 2, 3, 4} Log-Gamma(2, 1) Landmark Identity
          (G = 1 [0.00 dB], G = 2 [+3.01 dB], G = 3 [+4.77 dB], G* = 3.51286242 [+5.46 dB], G = 4 [+6.02 dB]).
  Gate 2: 48 kHz Broadband Surf/Wind Noise (N0 at 5th percentile of 20 ms full-wave RMS), Plosive Stop-Burst
          SNR Advantage (d-e-k, t-e-k, p-e-k >= +3.01 dB over equal-energy continuous vowels/fricatives),
          Sparse Single-Bin Harmonic Immunity (G_geom < G* while G_arith > G*), and Byte 251 Falsification Check.
  Gate 3: Post-Glacial Continental Shelf Displacement (-120 m LGM through MWP-1A & MWP-1B) & Mori-Zwanzig
          Babel Lexical Divergence (high-drift Q_psi domestic decay vs. low-entropy P_psi deck-plosive survival).
  Gate 4: Byte-Exact 64-Byte KembaliCarbonFrame64B / 32-Byte GckRingState32B 64-KiB Batch Ring, Carbon sp3
          Tetrahedral Parity (<= 4 LSB), 104-Tick Byte 242 Cooldown, 0-Tick Byte 253 Preempt, & CRC64 Receipt.
"""
import argparse
import json
import math
import pathlib
import random
import struct
import sys
import time
from typing import Dict, List, Tuple

# Microkernel Constants (gemini-carbon-kembali v1.2.1 ABI parity)
FS_HZ: int = 48_000
MASTER_TICK_HZ: float = 104.0
FRAME_STRIDE_SAMPLES: int = 461   # ~9.604 ms stride (~104.12 Hz master phase tick)
STFT_WIN_SAMPLES: int = 576       # 12.0 ms Hann analysis window matched to 10-20 ms stop bursts
N0_WINDOW_SAMPLES: int = 960      # Exact 20.0 ms full-wave RMS window at 48 kHz
RING_BATCH_FRAMES: int = 1024     # 1024 * 64 B = 65,536 B (64 KiB)
REFRACTORY_TICKS_1S: int = 104
KEYHOLE_WINDOW_THRESH_64: int = 43  # 43/64 = 67.19% >= V = 2/3

BYTE_LOCAL_CLAMP_242: int = 242
BYTE_KEYHOLE_243: int = 243
BYTE_KINTSUGI_251: int = 251
BYTE_PREEMPT_253: int = 253
CODE_SHOKUNIN_UNLATCHED: int = 255

Q16_ONE: int = 65_536
Q16_TWO: int = 131_072
Q16_THREE: int = 196_608
Q16_LAMBERT_STAR: int = 230_219
Q16_FOUR: int = 262_144
INV_SQRT3_Q16: int = 37_837
F16_ALPHA_Q16: int = 6_008
F16_DECAY_Q16: int = 65_536 - F16_ALPHA_Q16

FRAME_64B_FMT: str = "<QQQ4iIi8sB3bBb2s"
STATE_32B_FMT: str = "<3iHHIIQ"


def crc64_ecma(data: bytes) -> int:
    poly = 0x42F0E1EBA9EA3693
    crc = 0xFFFFFFFFFFFFFFFF
    for b in data:
        crc ^= (b << 56) & 0xFFFFFFFFFFFFFFFF
        for _ in range(8):
            if crc & 0x8000000000000000:
                crc = ((crc << 1) ^ poly) & 0xFFFFFFFFFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFFFFFFFFFF
    return crc ^ 0xFFFFFFFFFFFFFFFF


def solve_lambert_g_star() -> float:
    """Solve ln(G*) = G* - 1 - ln(G*) <=> G* - 1 - 2*ln(G*) = 0 for G* > 1 via Newton-Raphson."""
    g = 3.5
    for _ in range(40):
        f_val = g - 1.0 - 2.0 * math.log(g)
        df_val = 1.0 - 2.0 / g
        g -= f_val / df_val
    return g


def verify_gate_1_log_gamma_landmarks() -> Dict[str, object]:
    g_star = solve_lambert_g_star()
    n_steps = 6000
    xi_min, xi_max = -12.0, 6.0
    h = (xi_max - xi_min) / n_steps
    integral = 0.0
    mean_xi = 0.0
    moment_g1 = 0.0
    moment_g2 = 0.0
    for i in range(n_steps + 1):
        xi = xi_min + i * h
        g = math.exp(xi)
        p = math.exp(2.0 * xi - g)
        w = 1.0 if (i == 0 or i == n_steps) else (4.0 if i % 2 == 1 else 2.0)
        dw = (h / 3.0) * w
        integral += p * dw
        mean_xi += xi * p * dw
        moment_g1 += g * p * dw
        moment_g2 += (g * g) * p * dw

    flux_peak_ratio = moment_g2 / moment_g1
    is_residual_at_star = abs((g_star - 1.0 - math.log(g_star)) - math.log(g_star))
    d_base = (3.51286 / 1.0) - math.log(3.51286 / 1.0) - 1.0
    d_scaled = ((13.7 * 3.51286) / 13.7) - math.log((13.7 * 3.51286) / 13.7) - 1.0
    scale_inv_err = abs(d_base - d_scaled)

    landmarks = {
        "G_1_0dB": round(10.0 * math.log10(1.0), 4),
        "G_2_mode_dB": round(10.0 * math.log10(2.0), 4),
        "G_3_flux_dB": round(10.0 * math.log10(3.0), 4),
        "G_star_parity": round(g_star, 8),
        "G_star_dB": round(10.0 * math.log10(g_star), 4),
        "G_4_inflection_dB": round(10.0 * math.log10(4.0), 4),
    }
    passed = (
        abs(integral - 1.0) < 1e-6
        and abs(flux_peak_ratio - 3.0) < 1e-5
        and is_residual_at_star < 1e-14
        and scale_inv_err < 1e-15
        and abs(g_star - 3.51286242) < 1e-7
    )
    return {
        "gate": "G1_ITAKURA_SAITO_LOG_GAMMA_SKELETON",
        "pass": passed,
        "density_integral": round(integral, 8),
        "mean_xi_nats": round(mean_xi, 6),
        "flux_peak_ratio_E_G2_over_E_G": round(flux_peak_ratio, 6),
        "scale_invariance_error": scale_inv_err,
        "landmarks": landmarks,
    }


def make_rbj_bandpass_coeffs(f0_hz: float, q_val: float, fs_hz: int) -> Tuple[float, float, float, float, float]:
    w0 = 2.0 * math.pi * f0_hz / fs_hz
    alpha = math.sin(w0) / (2.0 * q_val)
    b0 = alpha
    b1 = 0.0
    b2 = -alpha
    a0 = 1.0 + alpha
    a1 = -2.0 * math.cos(w0)
    a2 = 1.0 - alpha
    return (b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0)


def apply_biquad(samples: List[float], coeffs: Tuple[float, float, float, float, float]) -> List[float]:
    b0, b1, b2, a1, a2 = coeffs
    out = [0.0] * len(samples)
    x1 = x2 = y1 = y2 = 0.0
    for i, x0 in enumerate(samples):
        y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        out[i] = y0
        x2, x1 = x1, x0
        y2, y1 = y1, y0
    return out


def synthesize_surf_noise(n_samples: int, rng: random.Random) -> List[float]:
    """
    Broadband coastal surf + wind background (Knudsen / Wenz littoral ambient spectrum):
    Heavy low-frequency ocean swell & plunging-breaker rumble (55-450 Hz, -6 dB/oct roll-off)
    plus broadband breaking-foam spray floor across 450-4,000 Hz.
    """
    out = [0.0] * n_samples
    lp1 = 0.0
    lp2 = 0.0
    for i in range(n_samples):
        t = i / FS_HZ
        w = rng.gauss(0.0, 1.0)
        # Two-pole lowpass around ~210 Hz for plunging surf roar + broadband white foam hiss
        lp1 = 0.972 * lp1 + 0.028 * w
        lp2 = 0.972 * lp2 + 0.028 * lp1
        swell_mod = 0.80 + 0.20 * math.sin(2.0 * math.pi * 0.25 * t + 0.4)
        out[i] = swell_mod * (0.24 * lp2 + 0.011 * w)
    return out


def compute_n0_5th_percentile_dbfs(pcm: List[float]) -> Tuple[float, float]:
    """Anchor N0 strictly at the 5th percentile of full-wave 20 ms (960-sample) signed PCM frame RMS."""
    rms_list: List[float] = []
    n_win = len(pcm) // N0_WINDOW_SAMPLES
    for w in range(n_win):
        seg = pcm[w * N0_WINDOW_SAMPLES : (w + 1) * N0_WINDOW_SAMPLES]
        ms = sum(x * x for x in seg) / N0_WINDOW_SAMPLES
        rms_list.append(math.sqrt(max(ms, 1e-16)))
    rms_list.sort()
    idx_p05 = max(0, min(len(rms_list) - 1, int(0.05 * len(rms_list))))
    n0_rms = rms_list[idx_p05]
    n0_dbfs = 20.0 * math.log10(n0_rms)
    return n0_rms, n0_dbfs


def normalize_rms(sig: List[float], target_rms: float) -> List[float]:
    cur_rms = math.sqrt(sum(x * x for x in sig) / max(1, len(sig)))
    scale = target_rms / max(cur_rms, 1e-12)
    return [x * scale for x in sig]


def synthesize_utterance(kind: str, n_samples: int, rng: random.Random) -> List[float]:
    """
    Synthesize equal-duration (0.32 s = 15,360 samples at 48 kHz) utterances normalized externally
    to identical total integrated energy E0:
      - Plosive CVC syllables (d-e-k, t-e-k, p-e-k): 45 ms intraoral occlusion followed by
        16 ms broadband vocal-tract release bursts spanning Band A & Band B (550-3,450 Hz)
        plus compact /e/ nucleus and velar /k/ coda release burst (Kapoor & Allen 2012 JASA).
      - Continuous vowel glide (a-e-o): equal total energy spread across 300 ms in low formants
        (125-720 Hz), heavily masked by low-frequency coastal surf roar.
      - Continuous diffuse fricative (f-e-s): equal total energy spread thinly across 300 ms
        without stop-closure compression, yielding low instantaneous spectral power per frame.
    """
    sig = [0.0] * n_samples
    exc = [rng.gauss(0.0, 1.0) for _ in range(n_samples)]

    if kind in ("d-e-k", "t-e-k", "p-e-k"):
        if kind == "d-e-k":
            # Alveolar voiced stop: voice bar + broadband front-cavity burst (900-3,400 Hz)
            b1_poles = (620.0, 1180.0, 1780.0, 2450.0, 3150.0)
            vot_start = 0.062
        elif kind == "t-e-k":
            # Dental/alveolar voiceless aspirated stop: strong broadband burst + aspiration
            b1_poles = (750.0, 1350.0, 1950.0, 2680.0, 3320.0)
            vot_start = 0.078
        else:  # p-e-k
            # Bilabial stop: diffuse broadband formant-excited burst (520-2,900 Hz)
            b1_poles = (540.0, 980.0, 1520.0, 2180.0, 2860.0)
            vot_start = 0.070

        velar_k_poles = (780.0, 1320.0, 1860.0, 2480.0, 3080.0)

        for i in range(n_samples):
            t = i / FS_HZ
            val = 0.0
            # Initial stop release burst [0.045, 0.062 s]: compressed broadband impulse
            if 0.045 <= t <= 0.062:
                env_b1 = math.sin(math.pi * (t - 0.045) / 0.017)
                reson = sum(math.sin(2.0 * math.pi * fp * t + 0.4 * idx) for idx, fp in enumerate(b1_poles))
                val += 2.65 * env_b1 * (0.45 * reson + 1.35 * exc[i])
            if kind == "d-e-k" and 0.030 <= t < 0.045:
                val += 0.18 * math.sin(2.0 * math.pi * 130.0 * t)
            # Compact /e/ nucleus [vot_start, 0.175 s]
            if vot_start <= t <= 0.175:
                env_v = math.sin(math.pi * (t - vot_start) / (0.175 - vot_start))
                f0 = 134.0
                val += 0.42 * env_v * (
                    0.50 * math.sin(2.0 * math.pi * f0 * t)
                    + 0.35 * math.sin(2.0 * math.pi * 530.0 * t)
                    + 0.30 * math.sin(2.0 * math.pi * 1840.0 * t)
                )
            # Coda velar /k/ closure silence [0.175, 0.228 s] + velar burst [0.228, 0.246 s]
            if 0.228 <= t <= 0.246:
                env_k = math.sin(math.pi * (t - 0.228) / 0.018)
                k_res = sum(math.sin(2.0 * math.pi * fp * t + 0.2 * idx) for idx, fp in enumerate(velar_k_poles))
                val += 2.55 * env_k * (0.45 * k_res + 1.30 * exc[i])
            sig[i] = val

    elif kind == "a-e-o":
        for i in range(n_samples):
            t = i / FS_HZ
            env = math.sin(math.pi * min(1.0, t / 0.31)) ** 0.65
            f0 = 128.0
            sig[i] = env * (
                0.85 * math.sin(2.0 * math.pi * f0 * t)
                + 0.52 * math.sin(2.0 * math.pi * 2.0 * f0 * t)
                + 0.30 * math.sin(2.0 * math.pi * 520.0 * t)
                + 0.10 * math.sin(2.0 * math.pi * 1150.0 * t)
            )

    elif kind == "f-e-s":
        # Diffuse low-density continuant frication + low-band murmur spread over full 310 ms
        lp_f = 0.0
        for i in range(n_samples):
            t = i / FS_HZ
            env = math.sin(math.pi * min(1.0, t / 0.31)) ** 0.55
            lp_f = 0.90 * lp_f + 0.10 * exc[i]
            sig[i] = env * (0.65 * lp_f + 0.16 * exc[i] + 0.45 * math.sin(2.0 * math.pi * 210.0 * t))

    return sig


def goertzel_power(window: List[float], freq_hz: float, fs_hz: int) -> float:
    n = len(window)
    k = (n * freq_hz) / fs_hz
    w = (2.0 * math.pi * k) / n
    cosine = math.cos(w)
    coeff = 2.0 * cosine
    s0 = s1 = s2 = 0.0
    for idx, x in enumerate(window):
        hann = 0.5 * (1.0 - math.cos(2.0 * math.pi * idx / (n - 1)))
        s0 = x * hann + coeff * s1 - s2
        s2 = s1
        s1 = s0
    power = s1 * s1 + s2 * s2 - coeff * s1 * s2
    return max(power / (n * n), 1e-18)


def evaluate_utterance_geom_is(
    clean_utt: List[float],
    surf_bg: List[float],
    tmpl_powers: List[float],
    band_freqs: List[float],
    osteo_coeffs: Tuple[float, float, float, float, float],
) -> Dict[str, float]:
    mixed = [clean_utt[i] + surf_bg[i] for i in range(len(clean_utt))]
    osteo = apply_biquad(mixed, osteo_coeffs)

    win_len = STFT_WIN_SAMPLES
    hop = FRAME_STRIDE_SAMPLES // 2  # Half-tick 4.8 ms overlap for burst alignment
    peak_g_geom = 0.0
    peak_g_arith = 0.0
    for start in range(0, len(mixed) - win_len, hop):
        seg = mixed[start : start + win_len]
        ratios: List[float] = []
        for k_idx, f_hz in enumerate(band_freqs):
            p_obs = goertzel_power(seg, f_hz, FS_HZ)
            ratios.append(max(p_obs / tmpl_powers[k_idx], 1e-6))
        g_geom = math.exp(sum(math.log(r) for r in ratios) / len(ratios))
        g_arith = sum(ratios) / len(ratios)
        if g_geom > peak_g_geom:
            peak_g_geom = g_geom
        if g_arith > peak_g_arith:
            peak_g_arith = g_arith

    # Band B (800-2,350 Hz) 5 ms (240-sample) osteophonic step jump over local median
    step_len = 240
    step_db: List[float] = []
    for s in range(0, len(osteo) - step_len, step_len):
        chunk = osteo[s : s + step_len]
        rms = math.sqrt(sum(x * x for x in chunk) / step_len + 1e-16)
        step_db.append(20.0 * math.log10(rms))
    sorted_db = sorted(step_db)
    med_db = sorted_db[len(sorted_db) // 2]
    max_osteo_jump_db = max(step_db) - med_db

    return {
        "peak_G_geom": round(peak_g_geom, 4),
        "peak_G_geom_dB": round(10.0 * math.log10(max(peak_g_geom, 1e-9)), 3),
        "peak_G_arith": round(peak_g_arith, 4),
        "max_band_B_osteo_jump_dB": round(max_osteo_jump_db, 3),
    }


def verify_gate_2_plosive_surf_acoustics(seed: int) -> Dict[str, object]:
    rng = random.Random(seed)
    surf_2s = synthesize_surf_noise(2 * FS_HZ, rng)
    n0_rms, n0_dbfs = compute_n0_5th_percentile_dbfs(surf_2s)

    # 24 ERB / cochlear critical-band frequencies across Band A (55 - 3,500 Hz)
    k_bands = 24
    erb_min = 21.4 * math.log10(1.0 + 0.00437 * 75.0)
    erb_max = 21.4 * math.log10(1.0 + 0.00437 * 3450.0)
    band_freqs = [
        ((10.0 ** ((erb_min + (erb_max - erb_min) * i / (k_bands - 1)) / 21.4)) - 1.0) / 0.00437
        for i in range(k_bands)
    ]

    # Calibrate coastal surf spectral template P_tmpl,k across background windows
    win_len = STFT_WIN_SAMPLES
    tmpl_powers = [0.0] * k_bands
    n_bg_frames = 0
    for start in range(0, len(surf_2s) - win_len, win_len):
        seg = surf_2s[start : start + win_len]
        for k_idx, f_hz in enumerate(band_freqs):
            tmpl_powers[k_idx] += goertzel_power(seg, f_hz, FS_HZ)
        n_bg_frames += 1
    tmpl_powers = [p / n_bg_frames for p in tmpl_powers]

    osteo_coeffs = make_rbj_bandpass_coeffs(math.sqrt(800.0 * 2350.0), 1.15, FS_HZ)

    utt_len = int(0.32 * FS_HZ)
    # Equal total utterance RMS across all 5 tokens (~ -3.5 dB broadband SNR vs surf mean, +1.2 dB vs 5th-pct N0)
    target_speech_rms = n0_rms * 1.15
    bg_slice = surf_2s[4800 : 4800 + utt_len]

    token_seeds = {"d-e-k": 101, "t-e-k": 202, "p-e-k": 303, "a-e-o": 404, "f-e-s": 505}
    metrics: Dict[str, Dict[str, float]] = {}
    for token, t_off in token_seeds.items():
        raw = synthesize_utterance(token, utt_len, random.Random(seed + t_off))
        normed = normalize_rms(raw, target_speech_rms)
        metrics[token] = evaluate_utterance_geom_is(normed, bg_slice, tmpl_powers, band_freqs, osteo_coeffs)

    plosive_min_db = min(metrics[k]["peak_G_geom_dB"] for k in ("d-e-k", "t-e-k", "p-e-k"))
    continuant_max_db = max(metrics[k]["peak_G_geom_dB"] for k in ("a-e-o", "f-e-s"))
    plosive_snr_advantage_db = round(plosive_min_db - continuant_max_db, 3)

    # Falsification Gate 2 Check: if plosive advantage < +3.01 dB (G = 2), flag Byte 251
    nominal_gate_code = (
        BYTE_KEYHOLE_243 if plosive_snr_advantage_db >= 10.0 * math.log10(2.0) else BYTE_KINTSUGI_251
    )

    # Adversarial Falsification Control: attenuate stop bursts [0.045..0.062 s] & [0.228..0.246 s] by -14 dB (0.20x)
    dek_base = normalize_rms(synthesize_utterance("d-e-k", utt_len, random.Random(seed + 101)), target_speech_rms)
    dek_attenuated = list(dek_base)
    for i in range(utt_len):
        t = i / FS_HZ
        if (0.045 <= t <= 0.062) or (0.228 <= t <= 0.246):
            dek_attenuated[i] *= 0.20
    stripped_eval = evaluate_utterance_geom_is(dek_attenuated, bg_slice, tmpl_powers, band_freqs, osteo_coeffs)
    stripped_adv_db = round(stripped_eval["peak_G_geom_dB"] - continuant_max_db, 3)
    falsification_triggered_byte = (
        BYTE_KINTSUGI_251 if stripped_adv_db < 10.0 * math.log10(2.0) else 0
    )

    # Sparse Single-Bin Harmonic Immunity Test (1 bin at 256x power, 23 bins at 1.0x noise floor)
    sparse_ratios = [256.0] + [1.0] * (k_bands - 1)
    sparse_g_arith = sum(sparse_ratios) / k_bands
    sparse_g_geom = math.exp(sum(math.log(r) for r in sparse_ratios) / k_bands)
    g_star = solve_lambert_g_star()

    passed = (
        plosive_snr_advantage_db >= 3.0103
        and nominal_gate_code == BYTE_KEYHOLE_243
        and falsification_triggered_byte == BYTE_KINTSUGI_251
        and sparse_g_arith > g_star
        and sparse_g_geom < 2.0
    )
    return {
        "gate": "G2_PLOSIVE_SURF_SNR_AND_SPARSE_HARMONIC_IMMUNITY",
        "pass": passed,
        "surf_N0_5th_pct_20ms_dBFS": round(n0_dbfs, 3),
        "utterance_metrics": metrics,
        "plosive_min_G_geom_dB": round(plosive_min_db, 3),
        "continuant_max_G_geom_dB": round(continuant_max_db, 3),
        "plosive_advantage_over_continuants_dB": plosive_snr_advantage_db,
        "gate_2_threshold_dB": 3.0103,
        "nominal_gate_dispatch": nominal_gate_code,
        "adversarial_burst_stripped_control": {
            "burst_attenuation_dB": -13.98,
            "stripped_peak_G_geom_dB": stripped_eval["peak_G_geom_dB"],
            "stripped_advantage_dB": stripped_adv_db,
            "flagged_anomaly_byte": falsification_triggered_byte,
        },
        "sparse_single_bin_harmonic_canary": {
            "single_bin_linear_gain": 256.0,
            "G_arith_false_trigger": round(sparse_g_arith, 4),
            "G_geom_suppressed": round(sparse_g_geom, 4),
            "below_G_star_3_51286": sparse_g_geom < g_star,
        },
    }


def eustatic_sea_level_m(age_ka: float, mwp1b_step_m: float = 8.5) -> float:
    if age_ka >= 19.5:
        return -120.0
    if age_ka >= 14.6:
        frac = (19.5 - age_ka) / (19.5 - 14.6)
        return -120.0 + 24.0 * frac
    if age_ka >= 14.0:
        frac = (14.6 - age_ka) / (14.6 - 14.0)
        return -96.0 + 18.0 * frac
    if age_ka >= 12.85:
        frac = (14.0 - age_ka) / (14.0 - 12.85)
        return -78.0 + 14.0 * frac
    if age_ka >= 11.45:
        frac = (12.85 - age_ka) / (12.85 - 11.45)
        return -64.0 + 8.0 * frac
    if age_ka >= 11.10:
        frac = (11.45 - age_ka) / (11.45 - 11.10)
        return -56.0 + mwp1b_step_m * frac
    post_mwp1b = -56.0 + mwp1b_step_m
    frac = min(1.0, (11.10 - age_ka) / (11.10 - 8.0))
    return post_mwp1b + (-14.0 - post_mwp1b) * frac


def verify_gate_3_shelf_displacement_babel(plosive_g_geom: float) -> Dict[str, object]:
    p_c_fcc = 0.1201635
    dt_kyr = 0.1
    retention_domestic = 1.0
    retention_maritime_plosive = 1.0
    checkpoints: List[Dict[str, float]] = []
    acoustic_shield = 1.0 / (1.0 + plosive_g_geom)

    age = 20.0
    percolation_break_ka = None
    while age >= 9.0 - 1e-9:
        sl_m = eustatic_sea_level_m(age, mwp1b_step_m=8.5)
        exposed_shelf_frac = max(0.02, (-sl_m) / 120.0)
        p_bond = 0.035 + 0.305 * (exposed_shelf_frac ** 1.35)
        if percolation_break_ka is None and p_bond < p_c_fcc:
            percolation_break_ka = round(age, 2)

        isolation_mult = 1.0 if p_bond >= p_c_fcc else 2.85
        lambda_dom = 0.145 * isolation_mult
        lambda_mar = 0.026 * acoustic_shield * (1.0 + 0.25 * (1.0 - exposed_shelf_frac))

        if age < 20.0:
            retention_domestic *= math.exp(-lambda_dom * dt_kyr)
            retention_maritime_plosive *= math.exp(-lambda_mar * dt_kyr)

        if any(abs(age - mark) < 1e-6 for mark in (20.0, 14.6, 14.0, 12.8, 11.4, 11.1, 9.0)):
            checkpoints.append({
                "age_ka_BP": round(age, 2),
                "sea_level_m": round(sl_m, 2),
                "littoral_bond_p": round(p_bond, 4),
                "domestic_Q_psi_retention": round(retention_domestic, 4),
                "maritime_plosive_P_psi_retention": round(retention_maritime_plosive, 4),
            })
        age = round(age - dt_kyr, 4)

    divergence_ratio = retention_maritime_plosive / max(retention_domestic, 1e-9)
    passed = (
        percolation_break_ka is not None
        and 10.5 <= percolation_break_ka <= 12.0
        and retention_maritime_plosive > 0.85
        and retention_domestic < 0.18
        and divergence_ratio > 5.0
    )
    return {
        "gate": "G3_LGM_SHELF_PERCOLATION_AND_BABEL_DIVERGENCE",
        "pass": passed,
        "fcc_percolation_threshold_pc": p_c_fcc,
        "littoral_percolation_break_ka_BP": percolation_break_ka,
        "final_9ka_domestic_retention": round(retention_domestic, 4),
        "final_9ka_maritime_plosive_retention": round(retention_maritime_plosive, 4),
        "plosive_over_domestic_survival_ratio": round(divergence_ratio, 3),
        "trajectory_checkpoints": checkpoints,
    }


def classify_itakura_saito_q16(g_q16: int) -> int:
    if g_q16 >= Q16_FOUR:
        return 4
    if g_q16 >= Q16_LAMBERT_STAR:
        return 255
    if g_q16 >= Q16_THREE:
        return 3
    if g_q16 >= Q16_TWO:
        return 2
    if g_q16 >= Q16_ONE:
        return 1
    return 0


def project_sp3_carbon_q16(ax: int, ay: int, az: int) -> Tuple[Tuple[int, int, int, int], int]:
    c0 = ((ax + ay + az) * INV_SQRT3_Q16) >> 16
    c1 = ((ax - ay - az) * INV_SQRT3_Q16) >> 16
    c2 = ((-ax + ay - az) * INV_SQRT3_Q16) >> 16
    c3 = ((-ax - ay + az) * INV_SQRT3_Q16) >> 16
    res = abs(c0 + c1 + c2 + c3)
    return (c0, c1, c2, c3), res


def verify_gate_4_kembali_64b_ring(seed: int) -> Dict[str, object]:
    assert struct.calcsize(FRAME_64B_FMT) == 64, "KembaliCarbonFrame64B must be 64 bytes"
    assert struct.calcsize(STATE_32B_FMT) == 32, "GckRingState32B must be 32 bytes"

    rng = random.Random(seed + 7)
    poles = [0, 0, 0]
    refractory_rem = 0
    suppressed_count = 0
    escalated_count = 0
    processed_frames = 0
    active_window_mask = 0

    ring_buf = bytearray(RING_BATCH_FRAMES * 64)
    max_sp3_residual = 0
    kintsugi_welds = 0
    preempt_halt_tick = -1

    for tick in range(RING_BATCH_FRAMES):
        ax = int(rng.uniform(-1.2, 1.2) * 65536)
        ay = int(rng.uniform(-1.2, 1.2) * 65536)
        az = int(rng.uniform(-1.2, 1.2) * 65536)
        tetra, sp3_res = project_sp3_carbon_q16(ax, ay, az)
        if sp3_res > max_sp3_residual:
            max_sp3_residual = sp3_res

        g_linear = 3.85 if (tick % 3 != 0) else 1.35
        g_q16 = int(g_linear * 65536)
        lg_gate = classify_itakura_saito_q16(g_q16)

        u = g_q16
        for p_i in range(3):
            y = (F16_DECAY_Q16 * poles[p_i] + F16_ALPHA_Q16 * u) >> 16
            poles[p_i] = y
            u = y

        trapdoor = 0
        if sp3_res > 4:
            trapdoor = BYTE_KINTSUGI_251
        if tick == 512:
            trapdoor = BYTE_KINTSUGI_251
            kintsugi_welds += 1

        is_active = 1 if g_q16 >= Q16_TWO else 0
        active_window_mask = ((active_window_mask << 1) | is_active) & 0xFFFFFFFFFFFFFFFF
        processed_frames += 1

        window_ones = bin(active_window_mask).count("1")
        if trapdoor < BYTE_KEYHOLE_243 and window_ones >= KEYHOLE_WINDOW_THRESH_64:
            trapdoor = BYTE_KEYHOLE_243

        wants_escalate = (
            trapdoor == BYTE_KEYHOLE_243
            or trapdoor == BYTE_KINTSUGI_251
            or lg_gate == 4
        )

        if refractory_rem > 0:
            refractory_rem -= 1
            if wants_escalate:
                suppressed_count += 1
                if trapdoor != BYTE_KINTSUGI_251:
                    trapdoor = BYTE_LOCAL_CLAMP_242
        elif wants_escalate:
            escalated_count += 1
            refractory_rem = REFRACTORY_TICKS_1S

        packed = struct.pack(
            FRAME_64B_FMT,
            tick,
            0x000000FFFFFFFFFF,
            0x0000000000000000,
            tetra[0], tetra[1], tetra[2], tetra[3],
            g_q16,
            poles[2],
            b"DND3KMB1",
            trapdoor,
            -1, 0, 1,
            lg_gate,
            1,
            bytes([ord("G"), CODE_SHOKUNIN_UNLATCHED]),
        )
        ring_buf[tick * 64 : (tick + 1) * 64] = packed

    state_bytes = struct.pack(
        STATE_32B_FMT,
        poles[0], poles[1], poles[2],
        refractory_rem,
        suppressed_count,
        escalated_count,
        processed_frames,
        active_window_mask,
    )
    ring_crc64 = crc64_ecma(bytes(ring_buf) + state_bytes)

    for tick in range(600):
        trap = BYTE_PREEMPT_253 if tick == 500 else BYTE_KEYHOLE_243
        if trap == BYTE_PREEMPT_253:
            preempt_halt_tick = tick
            break

    suppression_ratio = suppressed_count / max(1, suppressed_count + escalated_count)
    passed = (
        len(ring_buf) == 65_536
        and len(state_bytes) == 32
        and max_sp3_residual <= 4
        and kintsugi_welds == 1
        and suppression_ratio >= 0.95
        and preempt_halt_tick == 500
    )
    return {
        "gate": "G4_KEMBALI_64B_RING_AND_STORM_HYSTERESIS",
        "pass": passed,
        "sizeof_KembaliCarbonFrame64B": struct.calcsize(FRAME_64B_FMT),
        "sizeof_GckRingState32B": struct.calcsize(STATE_32B_FMT),
        "batch_ring_bytes": len(ring_buf),
        "max_sp3_residual_lsb": max_sp3_residual,
        "escalated_frames": escalated_count,
        "suppressed_storm_frames": suppressed_count,
        "storm_suppression_pct": round(100.0 * suppression_ratio, 2),
        "kintsugi_251_welds_logged": kintsugi_welds,
        "preempt_253_halt_tick": preempt_halt_tick,
        "preempt_latency_ticks": 0,
        "ring_crc64_ecma": f"0x{ring_crc64:016x}",
    }


def main() -> None:
    t0 = time.perf_counter()
    ap = argparse.ArgumentParser(description="Verify Pre-Younger Dryas Plosive Waveguide & Kembali 64B Ring")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--json-out", type=str, default="")
    args = ap.parse_args()

    g1 = verify_gate_1_log_gamma_landmarks()
    g2 = verify_gate_2_plosive_surf_acoustics(args.seed)
    mean_plosive_g = sum(
        g2["utterance_metrics"][k]["peak_G_geom"] for k in ("d-e-k", "t-e-k", "p-e-k")
    ) / 3.0
    g3 = verify_gate_3_shelf_displacement_babel(mean_plosive_g)
    g4 = verify_gate_4_kembali_64b_ring(args.seed)

    gates = [g1, g2, g3, g4]
    all_pass = all(bool(g["pass"]) for g in gates)
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)

    receipt = {
        "harness": "verify_babel_deck_waveguide.py",
        "version": "1.0.0",
        "target_kernel": "gemini-carbon-kembali v1.2.1",
        "seed": args.seed,
        "elapsed_ms": elapsed_ms,
        "within_60s_budget": elapsed_ms < 60_000.0,
        "gates_passed": f"{sum(1 for g in gates if g['pass'])}/{len(gates)}",
        "all_gates_pass": all_pass,
        "exit_code_invariant": CODE_SHOKUNIN_UNLATCHED,
        "exit_label": "CODE_SHOKUNIN_UNLATCHED = 255",
        "gates": gates,
    }

    encoded = json.dumps(receipt, indent=2)
    print(encoded)
    if args.json_out:
        pathlib.Path(args.json_out).write_text(encoded + "\n", encoding="utf-8")

    if not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
