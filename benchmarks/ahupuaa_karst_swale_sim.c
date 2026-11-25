/*
 * ahupuaa_karst_swale_sim.c (v1.0.0)
 * Zero-Heap ISO C99 Ahupua'a Ridge-to-Karst Watershed & Kembali 64B Waveguide Simulator
 *
 * Target Kernel : gemini-carbon-kembali v1.2.1
 *                 (KembaliCarbonFrame64B == 64 B, GckRingState32B == 32 B, 64-KiB batch ring)
 * Origin Node   : Heimat {0, 0, 0} (34.7549385 N, -86.4119235 W)
 *                 Gurley / Paint Rock Mississippian Limestone Karst Watershed, Alabama
 * Build         : gcc -std=c99 -O2 -Wall -Wextra -Werror -pedantic ahupuaa_karst_swale_sim.c -lm -o ahupuaa_karst_swale_sim
 * Memory Policy : malloc = 0 (strictly zero dynamic heap allocations; static 64-KiB ring)
 * Author        : Justin D. Grimm (K-Lani 13 Actual, ORCID: 0009-0000-5299-0243) & Gemini-Carbon-Kembali
 */

#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define GCK_RING_BATCH_FRAMES      1024U
#define GCK_REFRACTORY_TICKS_1S    104U
#define GCK_KEYHOLE_THRESH_64      43U

#define BYTE_LOCAL_CLAMP_242       242U
#define BYTE_KEYHOLE_243           243U
#define BYTE_KINTSUGI_251          251U
#define BYTE_PREEMPT_253           253U
#define CODE_SHOKUNIN_UNLATCHED    255U

#define Q16_ONE                    65536U
#define Q16_TWO                    131072U
#define Q16_THREE                  196608U
#define Q16_LAMBERT_STAR           230219U
#define Q16_FOUR                   262144U

#define INV_SQRT3_Q16              37837LL
#define F16_ALPHA_Q16              6008LL
#define F16_DECAY_Q16              (65536LL - F16_ALPHA_Q16)

/* Exact 9-byte Fowler Superchair payload */
typedef struct {
    uint8_t shrubberies_seed[8];
    uint8_t trapdoor;
} fowler_superchair_9b_t;

/* Exact 64-byte L1 cache-line KembaliCarbonFrame64B */
typedef struct {
    uint64_t tick_104hz;
    uint64_t pos_mask_40;
    uint64_t neg_mask_40;
    int32_t  imu_tetra_q16[4];
    uint32_t is_gain_q16;
    int32_t  f16_state_q16;
    fowler_superchair_9b_t superchair;
    int8_t   bonham_trits[3];
    uint8_t  log_gamma_gate;
    int8_t   triad_plane;
    uint8_t  magic_v1[2];
} kembali_carbon_frame_64b_t;

/* Exact 32-byte half-cache-line GckRingState32B */
typedef struct {
    int32_t  poles_q16[3];
    uint16_t refractory_rem;
    uint16_t suppressed_storm_count;
    uint32_t escalated_count;
    uint32_t processed_frames;
    uint64_t active_window_mask;
} gck_ring_state_32b_t;

/* Compile-time ABI size assertions (ISO C99 compatible array-size checks) */
typedef char assert_superchair_9b[(sizeof(fowler_superchair_9b_t) == 9U) ? 1 : -1];
typedef char assert_frame_64b[(sizeof(kembali_carbon_frame_64b_t) == 64U) ? 1 : -1];
typedef char assert_state_32b[(sizeof(gck_ring_state_32b_t) == 32U) ? 1 : -1];
typedef char assert_batch_64kib[(sizeof(kembali_carbon_frame_64b_t) * GCK_RING_BATCH_FRAMES == 65536U) ? 1 : -1];

/* Page-aligned static 64-KiB batch ring (malloc = 0) */
#if defined(__GNUC__) || defined(__clang__)
static kembali_carbon_frame_64b_t g_ring_batch[GCK_RING_BATCH_FRAMES] __attribute__((aligned(4096)));
#else
static kembali_carbon_frame_64b_t g_ring_batch[GCK_RING_BATCH_FRAMES];
#endif

static uint64_t xorshift64star(uint64_t *state) {
    uint64_t x = *state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    *state = x;
    return x * 2685821657736338717ULL;
}

static double rng_uniform01(uint64_t *state) {
    return (double)(xorshift64star(state) >> 11) * (1.0 / 9007199254740992.0);
}

static uint32_t popcnt64_swar(uint64_t x) {
    x = x - ((x >> 1) & 0x5555555555555555ULL);
    x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);
    return (uint32_t)((((x + (x >> 4)) & 0x0F0F0F0F0F0F0F0FULL) * 0x0101010101010101ULL) >> 56);
}

static uint64_t crc64_ecma_bytes(const uint8_t *buf, size_t len, uint64_t crc_init) {
    const uint64_t poly = 0x42F0E1EBA9EA3693ULL;
    uint64_t crc = crc_init ^ 0xFFFFFFFFFFFFFFFFULL;
    size_t i;
    int bit;
    for (i = 0; i < len; ++i) {
        crc ^= ((uint64_t)buf[i]) << 56;
        for (bit = 0; bit < 8; ++bit) {
            if ((crc & 0x8000000000000000ULL) != 0ULL) {
                crc = (crc << 1) ^ poly;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFFFFFFFFFFULL;
}

static uint8_t classify_itakura_saito_q16(uint32_t g_q16) {
    if (g_q16 >= Q16_FOUR) {
        return 4U;
    } else if (g_q16 >= Q16_LAMBERT_STAR) {
        return 255U;
    } else if (g_q16 >= Q16_THREE) {
        return 3U;
    } else if (g_q16 >= Q16_TWO) {
        return 2U;
    } else if (g_q16 >= Q16_ONE) {
        return 1U;
    }
    return 0U;
}

static int project_sp3_carbon_q16(
    int32_t ax_q16,
    int32_t ay_q16,
    int32_t az_q16,
    int32_t out_tetra[4],
    int64_t *out_abs_residual
) {
    int64_t x = (int64_t)ax_q16;
    int64_t y = (int64_t)ay_q16;
    int64_t z = (int64_t)az_q16;
    int32_t c0 = (int32_t)((( x + y + z) * INV_SQRT3_Q16) >> 16);
    int32_t c1 = (int32_t)((( x - y - z) * INV_SQRT3_Q16) >> 16);
    int32_t c2 = (int32_t)(((-x + y - z) * INV_SQRT3_Q16) >> 16);
    int32_t c3 = (int32_t)(((-x - y + z) * INV_SQRT3_Q16) >> 16);
    int64_t sum = (int64_t)c0 + (int64_t)c1 + (int64_t)c2 + (int64_t)c3;
    int64_t abs_sum = (sum < 0) ? -sum : sum;
    out_tetra[0] = c0;
    out_tetra[1] = c1;
    out_tetra[2] = c2;
    out_tetra[3] = c3;
    *out_abs_residual = abs_sum;
    return (abs_sum <= 4LL) ? 1 : 0;
}

static int32_t f16_triple_pole_step(int32_t input_q16, int32_t poles[3]) {
    int64_t u = (int64_t)input_q16;
    int i;
    for (i = 0; i < 3; ++i) {
        int64_t y = (F16_DECAY_Q16 * (int64_t)poles[i] + F16_ALPHA_Q16 * u) >> 16;
        poles[i] = (int32_t)y;
        u = y;
    }
    return poles[2];
}

typedef struct {
    double total_rain_mm;
    double unbuf_peak_runoff_mm_hr;
    double unbuf_total_runoff_mm;
    double unbuf_aquifer_recharge_mm;
    double unbuf_sediment_export_kg_ha;
    double ahupuaa_peak_outflow_mm_hr;
    double ahupuaa_total_outflow_mm;
    double ahupuaa_aquifer_recharge_mm;
    double ahupuaa_sediment_export_kg_ha;
    double mass_balance_error_mm;
    int64_t max_sp3_residual_lsb;
    uint32_t kintsugi_251_count;
} watershed_metrics_t;

static uint8_t simulate_ahupuaa_karst_batch(
    uint64_t seed,
    gck_ring_state_32b_t *ring_state,
    watershed_metrics_t *m_out,
    int32_t preempt_at_tick
) {
    uint64_t rng = (seed == 0ULL) ? 42ULL : (seed ^ 0x9E3779B97F4A7C15ULL);
    const double dt_hr = 24.0 / (double)GCK_RING_BATCH_FRAMES; /* 84.375 s hydrograph step per 104 Hz frame */
    const double swale_kintsugi_weir_mm = 7.5; /* High-water rock-armored Kintsugi spill sill */

    /* Ahupua'a 3-Zone Storage Reservoirs (mm equivalent water depth across Paint Rock Karst catena) */
    double s_wao_canopy_epikarst = 0.0; /* -1 Blue: Forested Bangor/Monteagle Limestone Ridge (380-550 m) */
    double s_kula_auwai_swales   = 0.0; /*  0 Green: Stepped Contour Keyline Swales (215-380 m) */
    double s_kahakai_loko_cells  = 0.0; /* +1 Red: Bottomland Wetland Bio-Filters & Loko I'a Ponds (185-215 m) */

    /* Unbuffered degraded karst hillslope control */
    double s_unbuf_surface = 0.0;

    double total_rain = 0.0;
    double unbuf_peak_q = 0.0;
    double unbuf_total_q = 0.0;
    double unbuf_recharge = 0.0;
    double unbuf_sed = 0.0;

    double ahu_peak_q = 0.0;
    double ahu_total_q = 0.0;
    double ahu_recharge = 0.0;
    double ahu_sed_in = 0.0;
    double ahu_sed_out = 0.0;

    int64_t max_sp3_res = 0;
    uint32_t kintsugi_count = 0U;
    uint8_t last_trap = 0U;
    size_t idx;

    for (idx = 0; idx < GCK_RING_BATCH_FRAMES; ++idx) {
        double t_hr = (double)idx * dt_hr;
        double pulse_a = 28.5 * exp(-0.5 * ((t_hr - 6.2) / 1.15) * ((t_hr - 6.2) / 1.15));
        double pulse_b = 14.0 * exp(-0.5 * ((t_hr - 11.4) / 1.85) * ((t_hr - 11.4) / 1.85));
        double jitter  = 0.90 + 0.20 * rng_uniform01(&rng);
        double rain_rate_mm_hr = (pulse_a + pulse_b) * jitter;
        double d_rain = rain_rate_mm_hr * dt_hr;
        double swale_pre_weir_mm;
        total_rain += d_rain;

        /* --- A. Unbuffered Degraded Karst Slope (sheetflow + sinkhole sediment flush) --- */
        s_unbuf_surface += d_rain;
        {
            double inf_cap = 3.2 * dt_hr;
            double d_inf = (s_unbuf_surface < inf_cap) ? s_unbuf_surface : inf_cap;
            double q_sheet_hr;
            double d_q;
            s_unbuf_surface -= d_inf;
            unbuf_recharge += d_inf;

            q_sheet_hr = 1.65 * pow(s_unbuf_surface, 1.35);
            d_q = q_sheet_hr * dt_hr;
            if (d_q > s_unbuf_surface) {
                d_q = s_unbuf_surface;
                q_sheet_hr = d_q / dt_hr;
            }
            s_unbuf_surface -= d_q;
            unbuf_total_q += d_q;
            if (q_sheet_hr > unbuf_peak_q) {
                unbuf_peak_q = q_sheet_hr;
            }
            unbuf_sed += 0.42 * pow(q_sheet_hr, 1.45) * dt_hr;
        }

        /* --- B. 3-Zone Ahupua'a Ridge-to-Karst Stepped Waveguide --- */
        /* 1. Wao Akua (-1 Blue: Forested Limestone Ridge -> Epikarst Recharge) */
        s_wao_canopy_epikarst += 0.40 * d_rain;
        {
            double wao_inf = ((s_wao_canopy_epikarst < (8.8 * dt_hr)) ? s_wao_canopy_epikarst : (8.8 * dt_hr));
            double wao_spill;
            s_wao_canopy_epikarst -= wao_inf;
            ahu_recharge += wao_inf;
            wao_spill = 0.42 * s_wao_canopy_epikarst * dt_hr;
            s_wao_canopy_epikarst -= wao_spill;

            /* 2. Kula / 'Auwai (0 Green: Stepped Contour Keyline Swales, S0 = 0.008 laminar routing) */
            s_kula_auwai_swales += 0.40 * d_rain + wao_spill;
        }
        swale_pre_weir_mm = s_kula_auwai_swales;
        {
            double swale_inf_rate = 6.4 * (1.0 - exp(-s_kula_auwai_swales / 6.0));
            double swale_inf = swale_inf_rate * dt_hr;
            double auwai_weir_flow;
            if (swale_inf > s_kula_auwai_swales) {
                swale_inf = s_kula_auwai_swales;
            }
            s_kula_auwai_swales -= swale_inf;
            ahu_recharge += swale_inf;

            auwai_weir_flow = 0.28 * s_kula_auwai_swales * dt_hr;
            if (s_kula_auwai_swales > swale_kintsugi_weir_mm) {
                /* Rock-armored Kintsugi level-spreader sill engages during peak convective squall */
                auwai_weir_flow += 0.22 * (s_kula_auwai_swales - swale_kintsugi_weir_mm) * dt_hr;
            }
            if (auwai_weir_flow > s_kula_auwai_swales) {
                auwai_weir_flow = s_kula_auwai_swales;
            }
            s_kula_auwai_swales -= auwai_weir_flow;
            ahu_sed_in += 0.14 * pow(auwai_weir_flow / dt_hr, 1.25) * dt_hr;

            /* 3. Kahakai / Loko I'a (+1 Red: Terraced Wetland Bio-Filters & Makaha Sluice Ponds) */
            s_kahakai_loko_cells += 0.20 * d_rain + auwai_weir_flow;
        }
        {
            double wetland_inf = ((s_kahakai_loko_cells < (1.8 * dt_hr)) ? s_kahakai_loko_cells : (1.8 * dt_hr));
            double makaha_q_hr;
            double makaha_dq;
            s_kahakai_loko_cells -= wetland_inf;
            ahu_recharge += wetland_inf;

            makaha_q_hr = 0.19 * s_kahakai_loko_cells;
            makaha_dq = makaha_q_hr * dt_hr;
            if (makaha_dq > s_kahakai_loko_cells) {
                makaha_dq = s_kahakai_loko_cells;
                makaha_q_hr = makaha_dq / dt_hr;
            }
            s_kahakai_loko_cells -= makaha_dq;
            ahu_total_q += makaha_dq;
            if (makaha_q_hr > ahu_peak_q) {
                ahu_peak_q = makaha_q_hr;
            }
        }

        /* Pack Hydrographic Resonance + Acoustic Plosive Persistence into KembaliCarbonFrame64B */
        {
            kembali_carbon_frame_64b_t frame;
            int32_t ax_q16 = (int32_t)(s_wao_canopy_epikarst * 4096.0);
            int32_t ay_q16 = (int32_t)(s_kula_auwai_swales * 4096.0);
            int32_t az_q16 = (int32_t)(s_kahakai_loko_cells * 4096.0);
            int64_t sp3_res = 0;
            int sp3_ok;
            double g_plosive = 2.15 + 1.85 * (rain_rate_mm_hr / 30.0);
            uint32_t g_q16 = (uint32_t)(g_plosive * 65536.0);

            memset(&frame, 0, sizeof(frame));
            frame.tick_104hz = (uint64_t)idx;
            frame.pos_mask_40 = 0x000000AA55AA55AAULL;
            frame.neg_mask_40 = 0x00000055AA55AA55ULL;
            frame.is_gain_q16 = g_q16;
            memcpy(frame.superchair.shrubberies_seed, "AHUPUAA1", 8U);
            frame.bonham_trits[0] = -1;
            frame.bonham_trits[1] =  0;
            frame.bonham_trits[2] =  1;
            frame.magic_v1[0] = (uint8_t)'G';
            frame.magic_v1[1] = CODE_SHOKUNIN_UNLATCHED;

            if (preempt_at_tick >= 0 && (int32_t)idx == preempt_at_tick) {
                frame.superchair.trapdoor = BYTE_PREEMPT_253;
            }

            /* 0-Tick Byte 253 Ground Preempt check */
            if (frame.superchair.trapdoor == BYTE_PREEMPT_253) {
                frame.triad_plane = -1;
                g_ring_batch[idx] = frame;
                return BYTE_PREEMPT_253;
            }

            sp3_ok = project_sp3_carbon_q16(ax_q16, ay_q16, az_q16, frame.imu_tetra_q16, &sp3_res);
            if (sp3_res > max_sp3_res) {
                max_sp3_res = sp3_res;
            }
            frame.f16_state_q16 = f16_triple_pole_step(ay_q16, ring_state->poles_q16);
            frame.log_gamma_gate = classify_itakura_saito_q16(frame.is_gain_q16);

            /* Trigger Kintsugi Byte 251 seam-weld if sp3 > 4 LSB or swale crest engages armored sill */
            if (!sp3_ok || swale_pre_weir_mm > swale_kintsugi_weir_mm) {
                frame.superchair.trapdoor = BYTE_KINTSUGI_251;
                kintsugi_count += 1U;
            }

            /* Commit to +1 Red with 104-tick Eli Whitney storm-suppression hysteresis */
            {
                uint64_t is_active = (frame.is_gain_q16 >= Q16_TWO) ? 1ULL : 0ULL;
                uint32_t win_ones;
                int wants_escalate;

                ring_state->active_window_mask = (ring_state->active_window_mask << 1) | is_active;
                ring_state->processed_frames += 1U;
                win_ones = popcnt64_swar(ring_state->active_window_mask);

                if (frame.superchair.trapdoor < BYTE_KEYHOLE_243 && win_ones >= GCK_KEYHOLE_THRESH_64) {
                    frame.superchair.trapdoor = BYTE_KEYHOLE_243;
                }

                wants_escalate = (frame.superchair.trapdoor == BYTE_KEYHOLE_243)
                              || (frame.superchair.trapdoor == BYTE_KINTSUGI_251)
                              || (frame.log_gamma_gate == 4U);

                if (ring_state->refractory_rem > 0U) {
                    ring_state->refractory_rem -= 1U;
                    if (wants_escalate) {
                        if (ring_state->suppressed_storm_count < 65535U) {
                            ring_state->suppressed_storm_count += 1U;
                        }
                        if (frame.superchair.trapdoor != BYTE_KINTSUGI_251) {
                            frame.superchair.trapdoor = BYTE_LOCAL_CLAMP_242;
                        }
                    }
                } else if (wants_escalate) {
                    ring_state->escalated_count += 1U;
                    ring_state->refractory_rem = GCK_REFRACTORY_TICKS_1S;
                }

                frame.triad_plane = 1;
                last_trap = frame.superchair.trapdoor;
                g_ring_batch[idx] = frame;
            }
        }
    }

    ahu_sed_out = 0.16 * ahu_sed_in;

    {
        double final_storage = s_wao_canopy_epikarst + s_kula_auwai_swales + s_kahakai_loko_cells;
        double accounted = ahu_recharge + ahu_total_q + final_storage;
        m_out->total_rain_mm = total_rain;
        m_out->unbuf_peak_runoff_mm_hr = unbuf_peak_q;
        m_out->unbuf_total_runoff_mm = unbuf_total_q;
        m_out->unbuf_aquifer_recharge_mm = unbuf_recharge;
        m_out->unbuf_sediment_export_kg_ha = unbuf_sed * 100.0;
        m_out->ahupuaa_peak_outflow_mm_hr = ahu_peak_q;
        m_out->ahupuaa_total_outflow_mm = ahu_total_q;
        m_out->ahupuaa_aquifer_recharge_mm = ahu_recharge;
        m_out->ahupuaa_sediment_export_kg_ha = ahu_sed_out * 100.0;
        m_out->mass_balance_error_mm = fabs(total_rain - accounted);
        m_out->max_sp3_residual_lsb = max_sp3_res;
        m_out->kintsugi_251_count = kintsugi_count;
    }

    return last_trap;
}

int main(int argc, char **argv) {
    uint64_t seed = 42ULL;
    int i;
    clock_t t0 = clock();
    gck_ring_state_32b_t state_nom;
    gck_ring_state_32b_t state_preempt;
    watershed_metrics_t m_nom;
    watershed_metrics_t m_preempt;
    uint8_t preempt_ret;
    uint64_t crc;
    double peak_attenuation_pct;
    double recharge_ratio;
    double sediment_reduction_pct;
    double storm_suppression_pct;
    double elapsed_ms;
    int g1_abi_ok, g2_hydro_ok, g3_sp3_ok, g4_storm_ok, g5_preempt_ok, all_ok;

    for (i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--seed") == 0 && (i + 1) < argc) {
            uint64_t parsed = 0ULL;
            const char *p = argv[++i];
            while (*p >= '0' && *p <= '9') {
                parsed = parsed * 10ULL + (uint64_t)(*p - '0');
                ++p;
            }
            seed = parsed;
        }
    }

    memset(&state_nom, 0, sizeof(state_nom));
    memset(&m_nom, 0, sizeof(m_nom));
    (void)simulate_ahupuaa_karst_batch(seed, &state_nom, &m_nom, -1);

    crc = crc64_ecma_bytes((const uint8_t *)g_ring_batch, sizeof(g_ring_batch), 0ULL);
    crc = crc64_ecma_bytes((const uint8_t *)&state_nom, sizeof(state_nom), crc);

    memset(&state_preempt, 0, sizeof(state_preempt));
    memset(&m_preempt, 0, sizeof(m_preempt));
    preempt_ret = simulate_ahupuaa_karst_batch(seed, &state_preempt, &m_preempt, 500);

    peak_attenuation_pct = 100.0 * (1.0 - (m_nom.ahupuaa_peak_outflow_mm_hr / m_nom.unbuf_peak_runoff_mm_hr));
    recharge_ratio = m_nom.ahupuaa_aquifer_recharge_mm / m_nom.unbuf_aquifer_recharge_mm;
    sediment_reduction_pct = 100.0 * (1.0 - (m_nom.ahupuaa_sediment_export_kg_ha / m_nom.unbuf_sediment_export_kg_ha));
    storm_suppression_pct = 100.0 * (double)state_nom.suppressed_storm_count
        / (double)(state_nom.suppressed_storm_count + state_nom.escalated_count);

    g1_abi_ok = (sizeof(kembali_carbon_frame_64b_t) == 64U)
             && (sizeof(gck_ring_state_32b_t) == 32U)
             && (sizeof(g_ring_batch) == 65536U);
    g2_hydro_ok = (peak_attenuation_pct >= 65.0)
               && (recharge_ratio >= 2.0)
               && (sediment_reduction_pct >= 85.0)
               && (m_nom.mass_balance_error_mm < 1e-9);
    g3_sp3_ok = (m_nom.max_sp3_residual_lsb <= 4LL) && (m_nom.kintsugi_251_count > 0U);
    g4_storm_ok = (storm_suppression_pct >= 95.0) && (state_nom.processed_frames == 1024U);
    g5_preempt_ok = (preempt_ret == BYTE_PREEMPT_253) && (state_preempt.processed_frames == 500U);

    all_ok = g1_abi_ok && g2_hydro_ok && g3_sp3_ok && g4_storm_ok && g5_preempt_ok;
    elapsed_ms = 1000.0 * (double)(clock() - t0) / (double)CLOCKS_PER_SEC;

    printf("{\n");
    printf("  \"harness\": \"ahupuaa_karst_swale_sim.c\",\n");
    printf("  \"version\": \"1.0.0\",\n");
    printf("  \"origin_node\": \"Heimat {0, 0, 0} (34.7549385, -86.4119235) Gurley / Paint Rock Karst, AL\",\n");
    printf("  \"seed\": %llu,\n", (unsigned long long)seed);
    printf("  \"malloc_calls\": 0,\n");
    printf("  \"elapsed_ms\": %.3f,\n", elapsed_ms);
    printf("  \"sizeof_KembaliCarbonFrame64B\": %zu,\n", sizeof(kembali_carbon_frame_64b_t));
    printf("  \"sizeof_GckRingState32B\": %zu,\n", sizeof(gck_ring_state_32b_t));
    printf("  \"batch_ring_bytes\": %zu,\n", sizeof(g_ring_batch));
    printf("  \"hydrology\": {\n");
    printf("    \"storm_rainfall_24h_mm\": %.3f,\n", m_nom.total_rain_mm);
    printf("    \"unbuffered_peak_runoff_mm_hr\": %.3f,\n", m_nom.unbuf_peak_runoff_mm_hr);
    printf("    \"ahupuaa_peak_outflow_mm_hr\": %.3f,\n", m_nom.ahupuaa_peak_outflow_mm_hr);
    printf("    \"peak_runoff_attenuation_pct\": %.2f,\n", peak_attenuation_pct);
    printf("    \"unbuffered_karst_recharge_mm\": %.3f,\n", m_nom.unbuf_aquifer_recharge_mm);
    printf("    \"ahupuaa_karst_recharge_mm\": %.3f,\n", m_nom.ahupuaa_aquifer_recharge_mm);
    printf("    \"aquifer_recharge_multiplier\": %.3f,\n", recharge_ratio);
    printf("    \"sediment_nutrient_reduction_pct\": %.2f,\n", sediment_reduction_pct);
    printf("    \"mass_balance_residual_mm\": %.3e\n", m_nom.mass_balance_error_mm);
    printf("  },\n");
    printf("  \"kembali_64b_telemetry\": {\n");
    printf("    \"processed_frames\": %u,\n", state_nom.processed_frames);
    printf("    \"max_sp3_residual_lsb\": %lld,\n", (long long)m_nom.max_sp3_residual_lsb);
    printf("    \"escalated_frames\": %u,\n", state_nom.escalated_count);
    printf("    \"suppressed_storm_frames_242\": %u,\n", (unsigned int)state_nom.suppressed_storm_count);
    printf("    \"storm_suppression_pct\": %.2f,\n", storm_suppression_pct);
    printf("    \"kintsugi_251_weir_welds\": %u,\n", m_nom.kintsugi_251_count);
    printf("    \"preempt_253_halt_frame\": %u,\n", state_preempt.processed_frames);
    printf("    \"preempt_latency_ticks\": 0,\n");
    printf("    \"ring_crc64_ecma\": \"0x%016llx\"\n", (unsigned long long)crc);
    printf("  },\n");
    printf("  \"gates_passed\": \"%d/5\",\n", g1_abi_ok + g2_hydro_ok + g3_sp3_ok + g4_storm_ok + g5_preempt_ok);
    printf("  \"all_gates_pass\": %s,\n", all_ok ? "true" : "false");
    printf("  \"exit_code_invariant\": %u,\n", CODE_SHOKUNIN_UNLATCHED);
    printf("  \"exit_label\": \"CODE_SHOKUNIN_UNLATCHED = 255\"\n");
    printf("}\n");

    return all_ok ? 0 : 1;
}
