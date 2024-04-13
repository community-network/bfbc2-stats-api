from enum import Enum

from pybfbc2stats import STATS_KEYS


class StringEnum(str, Enum):
    def __str__(self):
        return self.value


class ApiNamespace(StringEnum):
    # Expose namespaces by their real names
    battlefield = 'battlefield'
    cem_ea_id = 'cem_ea_id'
    ps3 = 'ps3'
    xbox = 'xbox'
    # Expose namespaces by modern, commonly used names
    psn = 'psn'
    xbl = 'xbl'
    pc = 'pc'
    # Expose namespaces by platforms
    ps4 = 'ps4'
    xbox360 = 'xbox360'
    xboxone = 'xboxone'


class ApiPlatform(StringEnum):
    pass


class FeslPlatform(ApiPlatform):
    pc = 'pc'
    ps3 = 'ps3'
    xbox360 = 'xbox360'


class TheaterPlatform(ApiPlatform):
    pc = 'pc'
    ps3 = 'ps3'


class FeslNamespace(bytes, Enum):
    battlefield = b'battlefield'
    cem_ea_id = b'cem_ea_id'
    ps3 = b'ps3'
    xbox = b'xbox'
    pc = b'cem_ea_id'
    psn = b'ps3'
    xbl = b'xbox'
    ps4 = b'ps3'
    xbox360 = b'xbox'
    xboxone = b'xbox'


class IdentifierType(StringEnum):
    playerName = 'byName'
    playerId = 'byId'


class StatsKeySet(StringEnum):
    all = 'all'
    default = 'default'
    minimal = 'minimal'
    weapons = 'weapons'
    vehicles = 'vehicles'


class LeaderboardSortKey(StringEnum):
    score = 'score'
    kills = 'kills'
    time = 'time'
    deaths = 'deaths'


DUMMY_TID = 0
LEADERBOARD_PAGE_SIZE = 50
STATS_KEY_SETS = {
    'all': STATS_KEYS,
    'default': [b'accuracy', b'c_40mmgl__kw_g', b'c_40mmgl__sfw_g', b'c_40mmgl__shw_g', b'c_40mmgl__sw_g',
                b'c_40mmsg__kw_g', b'c_40mmsg__sfw_g', b'c_40mmsg__shw_g', b'c_40mmsg__sw_g', b'c_9a91__kw_g',
                b'c_9a91__sfw_g', b'c_9a91__shw_g', b'c_9a91__sw_g', b'c_KORD__si_g', b'c_KORN__si_g', b'c_MI28__ddw_g',
                b'c_MI28__si_g', b'c_PBLB__ddw_g', b'c_PBLB__si_g', b'c_QLZ8__si_g', b'c_TOW2__si_g', b'c_VADS__si_g',
                b'c_XM307__si_g', b'c_XM312__si_g', b'c__40mmgl_hsh_g', b'c__40mmsg_hsh_g', b'c__9a91_hsh_g',
                b'c__KORD_ki_g', b'c__KORN_ki_g', b'c__MI28_ki_g', b'c__PBLB_ki_g', b'c__QLZ8_ki_g', b'c__TOW2_ki_g',
                b'c__VADS_ki_g', b'c__XM307_ki_g', b'c__XM312_ki_g', b'c___h_g', b'c___msa_g', b'c___r_g', b'c___res_g',
                b'c___rev_g', b'c___tag_g', b'c__aav_ki_g', b'c__aaw_hsh_g', b'c__aek_hsh_g', b'c__ah60_ki_g',
                b'c__ah64_ki_g', b'c__ak47v_hsh_g', b'c__aks74u_hsh_g', b'c__an94_hsh_g', b'c__as_ko_g',
                b'c__aug_hsh_g', b'c__bmd3_ki_g', b'c__bmda_ki_g', b'c__boaw_hsh_g', b'c__cav_ki_g', b'c__cobr_ki_g',
                b'c__de_ko_g', b'c__defi_hsh_g', b'c__f2000_hsh_g', b'c__g3_hsh_g', b'c__gaz69v_ki_g', b'c__gol_hsh_g',
                b'c__havoc_ki_g', b'c__helw_hsh_g', b'c__hmv_ki_g', b'c__hueyv_ki_g', b'c__jets_ki_g', b'c__m15v_ki_g',
                b'c__m16_hsh_g', b'c__m16a1v_hsh_g', b'c__m16k_hsh_g', b'c__m1911_hsh_g', b'c__m1_hsh_g',
                b'c__m1a1_hsh_g', b'c__m1a2_ki_g', b'c__m21v_hsh_g', b'c__m249_hsh_g', b'c__m24_hsh_g', b'c__m2v_hsh_g',
                b'c__m3a3_ki_g', b'c__m40v_hsh_g', b'c__m416_hsh_g', b'c__m48v_ki_g', b'c__m60_hsh_g', b'c__m60v_hsh_g',
                b'c__m93r_hsh_g', b'c__m95_hsh_g', b'c__m95k_hsh_g', b'c__m9_hsh_g', b'c__mac10v_hsh_g',
                b'c__mcs_hsh_g', b'c__mg36_hsh_g', b'c__mg3_hsh_g', b'c__mg3k_hsh_g', b'c__mk14ebr_hsh_g',
                b'c__mp412_hsh_g', b'c__n2k_hsh_g', b'c__pbrv_ki_g', b'c__pkm_hsh_g', b'c__pp2_hsh_g',
                b'c__ppshv_hsh_g', b'c__prtg_hsh_g', b'c__qbu88_hsh_g', b'c__qju88_hsh_g', b'c__quad_ki_g',
                b'c__re_ko_g', b'c__rept_hsh_g', b'c__rpkv_hsh_g', b'c__s12k_hsh_g', b'c__scar_hsh_g', b'c__smol_hsh_g',
                b'c__spas12_hsh_g', b'c__stgl_hsh_g', b'c__stmg_hsh_g', b'c__su_ko_g', b'c__sv98_hsh_g',
                b'c__svdv_hsh_g', b'c__svu_hsh_g', b'c__t54v_ki_g', b'c__t90_ki_g', b'c__tanc_hsh_g', b'c__tanm_hsh_g',
                b'c__tt33v_hsh_g', b'c__u12_hsh_g', b'c__uav_ki_g', b'c__ump_hsh_g', b'c__umpk_hsh_g', b'c__uzi_hsh_g',
                b'c__vodn_ki_g', b'c__vss_hsh_g', b'c__xm22v_hsh_g', b'c__xm8_hsh_g', b'c__xm8c_hsh_g',
                b'c__xm8lmg_hsh_g', b'c_aav__si_g', b'c_aaw__kw_g', b'c_aek__kw_g', b'c_aek__sfw_g', b'c_aek__shw_g',
                b'c_aek__sw_g', b'c_ah60__ddw_g', b'c_ah60__si_g', b'c_ah64__ddw_g', b'c_ah64__si_g', b'c_ak47v__kw_g',
                b'c_ak47v__sfw_g', b'c_ak47v__shw_g', b'c_ak47v__sw_g', b'c_aks74u__kw_g', b'c_aks74u__sfw_g',
                b'c_aks74u__shw_g', b'c_aks74u__sw_g', b'c_ammb__kw_g', b'c_ammb__sfw_g', b'c_ammb__shw_g',
                b'c_ammb__sw_g', b'c_an94__kw_g', b'c_an94__sfw_g', b'c_an94__shw_g', b'c_an94__sw_g', b'c_as__da_g',
                b'c_atm__kw_g', b'c_atm__sfw_g', b'c_atm__shw_g', b'c_atm__sw_g', b'c_aug__kw_g', b'c_aug__sfw_g',
                b'c_aug__shw_g', b'c_aug__sw_g', b'c_bmd3__ddw_g', b'c_bmd3__si_g', b'c_bmda__ddw_g', b'c_bmda__si_g',
                b'c_boaw__kw_g', b'c_c4__kw_g', b'c_c4__sfw_g', b'c_c4__shw_g', b'c_c4__sw_g', b'c_cav__ddw_g',
                b'c_cav__si_g', b'c_cobr__ddw_g', b'c_cobr__si_g', b'c_de__da_g', b'c_defi__kw_g', b'c_defi__sfw_g',
                b'c_defi__shw_g', b'c_defi__sw_g', b'c_deml__kw_g', b'c_f2000__kw_g', b'c_f2000__sfw_g',
                b'c_f2000__shw_g', b'c_f2000__sw_g', b'c_g3__kw_g', b'c_g3__sfw_g', b'c_g3__shw_g', b'c_g3__sw_g',
                b'c_gol__kw_g', b'c_gol__sfw_g', b'c_gol__shw_g', b'c_gol__sw_g', b'c_gaz69v__ddw_g', b'c_gaz69v__si_g',
                b'c_havoc__ddw_g', b'c_havoc__si_g', b'c_helw__kw_g', b'c_hgr__kw_g', b'c_hgr__sfw_g', b'c_hgr__shw_g',
                b'c_hgr__sw_g', b'c_hmv__ddw_g', b'c_hmv__si_g', b'c_hueyv__ddw_g', b'c_hueyv__si_g', b'c_jets__ddw_g',
                b'c_jets__si_g', b'c_knv__kw_g', b'c_knv__sfw_g', b'c_knv__shw_g', b'c_knv__sw_g', b'c_kuro__ddw_g',
                b'c_kuro__si_g', b'c_loss_att_out_g', b'c_loss_def_out_g', b'c_m136__kw_g', b'c_m136__sfw_g',
                b'c_m136__shw_g', b'c_m136__sw_g', b'c_m14v__sw_g', b'c_m15v__ddw_g', b'c_m15v__si_g', b'c_m16__kw_g',
                b'c_m16__sfw_g', b'c_m16__shw_g', b'c_m16__sw_g', b'c_m16a1v__kw_g', b'c_m16a1v__sfw_g',
                b'c_m16a1v__shw_g', b'c_m16a1v__sw_g', b'c_m16k__kw_g', b'c_m16k__sfw_g', b'c_m16k__shw_g',
                b'c_m16k__sw_g', b'c_m1911__kw_g', b'c_m1911__sfw_g', b'c_m1911__shw_g', b'c_m1911__sw_g',
                b'c_m1__kw_g', b'c_m1__sfw_g', b'c_m1__shw_g', b'c_m1__sw_g', b'c_m1a1__kw_g', b'c_m1a1__sfw_g',
                b'c_m1a1__shw_g', b'c_m1a1__sw_g', b'c_m1a2__ddw_g', b'c_m1a2__si_g', b'c_m21v__kw_g', b'c_m21v__sfw_g',
                b'c_m21v__shw_g', b'c_m21v__sw_g', b'c_m249__kw_g', b'c_m249__sfw_g', b'c_m249__shw_g', b'c_m249__sw_g',
                b'c_m24__kw_g', b'c_m24__sfw_g', b'c_m24__shw_g', b'c_m24__sw_g', b'c_m2cg__kw_g', b'c_m2cg__sfw_g',
                b'c_m2cg__shw_g', b'c_m2cg__sw_g', b'c_m2v__kw_g', b'c_m2v__sfw_g', b'c_m2v__shw_g', b'c_m2v__sw_g',
                b'c_m3a3__ddw_g', b'c_m3a3__si_g', b'c_m40v__kw_g', b'c_m40v__sfw_g', b'c_m40v__shw_g', b'c_m40v__sw_g',
                b'c_m416__kw_g', b'c_m416__sfw_g', b'c_m416__shw_g', b'c_m416__sw_g', b'c_m48v__ddw_g', b'c_m48v__si_g',
                b'c_m60__kw_g', b'c_m60__sfw_g', b'c_m60__shw_g', b'c_m60__sw_g', b'c_m60v__kw_g', b'c_m60v__sfw_g',
                b'c_m60v__shw_g', b'c_m60v__sw_g', b'c_m93r__kw_g', b'c_m93r__sfw_g', b'c_m93r__shw_g', b'c_m93r__sw_g',
                b'c_m95__kw_g', b'c_m95__sfw_g', b'c_m95__shw_g', b'c_m95__sw_g', b'c_m95k__kw_g', b'c_m95k__sfw_g',
                b'c_m95k__shw_g', b'c_m95k__sw_g', b'c_m9__kw_g', b'c_m9__sfw_g', b'c_m9__shw_g', b'c_m9__sw_g',
                b'c_mac10v__kw_g', b'c_mac10v__sfw_g', b'c_mac10v__shw_g', b'c_mac10v__sw_g', b'c_mcs__kw_g',
                b'c_mcs__sfw_g', b'c_mcs__shw_g', b'c_mcs__sw_g', b'c_mg36__kw_g', b'c_mg36__sfw_g', b'c_mg36__shw_g',
                b'c_mg36__sw_g', b'c_mg3__kw_g', b'c_mg3__sfw_g', b'c_mg3__shw_g', b'c_mg3__sw_g', b'c_mg3k__kw_g',
                b'c_mg3k__sfw_g', b'c_mg3k__shw_g', b'c_mg3k__sw_g', b'c_minitruckv__ddw_g', b'c_minitruckv__si_g',
                b'c_mk14ebr__kw_g', b'c_mk14ebr__sfw_g', b'c_mk14ebr__shw_g', b'c_mk14ebr__sw_g', b'c_mots__kw_g',
                b'c_mots__sfw_g', b'c_mots__shw_g', b'c_mots__sw_g', b'c_mp412__kw_g', b'c_mp412__sfw_g',
                b'c_mp412__shw_g', b'c_mp412__sw_g', b'c_mp443__sfw_g', b'c_mp443__shw_g', b'c_mp443__sw_g',
                b'c_mst__kw_g', b'c_mst__sfw_g', b'c_mst__shw_g', b'c_mst__sw_g', b'c_n2k__kw_g', b'c_n2k__sfw_g',
                b'c_n2k__shw_g', b'c_n2k__sw_g', b'c_pbrv__ddw_g', b'c_pbrv__si_g', b'c_pkm__kw_g', b'c_pkm__sfw_g',
                b'c_pkm__shw_g', b'c_pkm__sw_g', b'c_pp2__kw_g', b'c_pp2__sfw_g', b'c_pp2__shw_g', b'c_pp2__sw_g',
                b'c_ppshv__kw_g', b'c_ppshv__sfw_g', b'c_ppshv__shw_g', b'c_ppshv__sw_g', b'c_prtg__kw_g',
                b'c_qbu88__kw_g', b'c_qbu88__sfw_g', b'c_qbu88__shw_g', b'c_qbu88__sw_g', b'c_qju88__kw_g',
                b'c_qju88__sfw_g', b'c_qju88__shw_g', b'c_qju88__sw_g', b'c_quad__ddw_g', b'c_quad__si_g',
                b'c_re__da_g', b'c_rept__kw_g', b'c_rept__sfw_g', b'c_rept__shw_g', b'c_rept__sw_g',
                b'c_rok_MI28_kwi_g', b'c_rok_PBLB_kwi_g', b'c_rok__kw_g', b'c_rok_ah60_kwi_g', b'c_rok_ah64_kwi_g',
                b'c_rok_bmd3_kwi_g', b'c_rok_bmda_kwi_g', b'c_rok_cav_kwi_g', b'c_rok_havoc_kwi_g', b'c_rok_hmv_kwi_g',
                b'c_rok_m15v_kwi_g', b'c_rok_m1a2_kwi_g', b'c_rok_m3a3_kwi_g', b'c_rok_m48v_kwi_g', b'c_rok_quad_kwi_g',
                b'c_rok_t54v_kwi_g', b'c_rok_t90_kwi_g', b'c_rok_uav_kwi_g', b'c_rok_vodn_kwi_g', b'c_rpg7__kw_g',
                b'c_rpg7__sfw_g', b'c_rpg7__shw_g', b'c_rpg7__sw_g', b'c_rpkv__kw_g', b'c_rpkv__sfw_g',
                b'c_rpkv__shw_g', b'c_rpkv__sw_g', b'c_s12k__kw_g', b'c_s12k__sfw_g', b'c_s12k__shw_g', b'c_s12k__sw_g',
                b'c_scar__kw_g', b'c_scar__sfw_g', b'c_scar__shw_g', b'c_scar__sw_g', b'c_smol__kw_g', b'c_smol__sfw_g',
                b'c_smol__shw_g', b'c_smol__sw_g', b'c_spas12__kw_g', b'c_spas12__sfw_g', b'c_spas12__shw_g',
                b'c_spas12__sw_g', b'c_stgl__kw_g', b'c_stmg__kw_g', b'c_strl__kw_g', b'c_su__da_g', b'c_sv98__kw_g',
                b'c_sv98__sfw_g', b'c_sv98__shw_g', b'c_sv98__sw_g', b'c_svdv__kw_g', b'c_svdv__sfw_g',
                b'c_svdv__shw_g', b'c_svdv__sw_g', b'c_svu__kw_g', b'c_svu__sfw_g', b'c_svu__shw_g', b'c_svu__sw_g',
                b'c_t54v__ddw_g', b'c_t54v__si_g', b'c_t90__ddw_g', b'c_t90__si_g', b'c_trad__sfw_g', b'c_trad__sw_g',
                b'c_tru__ddw_g', b'c_tru__si_g', b'c_tt33v__kw_g', b'c_tt33v__sfw_g', b'c_tt33v__shw_g',
                b'c_tt33v__sw_g', b'c_u12__kw_g', b'c_u12__sfw_g', b'c_u12__shw_g', b'c_u12__sw_g', b'c_uav__ddw_g',
                b'c_uav__si_g', b'c_ump__kw_g', b'c_ump__sfw_g', b'c_ump__shw_g', b'c_ump__sw_g', b'c_umpk__kw_g',
                b'c_umpk__sfw_g', b'c_umpk__shw_g', b'c_umpk__sw_g', b'c_uzi__kw_g', b'c_uzi__sfw_g', b'c_uzi__shw_g',
                b'c_uzi__sw_g', b'c_uziv__sfw_g', b'c_uziv__sw_g', b'c_vodn__ddw_g', b'c_vodn__si_g', b'c_vss__kw_g',
                b'c_vss__sfw_g', b'c_vss__shw_g', b'c_vss__sw_g', b'c_vta01_win_nam02_outon_g',
                b'c_vta01_win_nam03_outon_g', b'c_vta01_win_nam05_outon_g', b'c_vta01_win_nam06_outon_g',
                b'c_vta04__gaz69v_ki_g', b'c_vta04__hueyv_ki_g', b'c_vta04__m15v_ki_g', b'c_vta04__m48v_ki_g',
                b'c_vta04__pbrv_ki_g', b'c_vta04__t54v_ki_g', b'c_vta05__tankv_ki_g', b'c_vta06__hueyv_ki_g',
                b'c_win_att_out_g', b'c_win_def_out_g', b'c_xm22v__kw_g', b'c_xm22v__sfw_g', b'c_xm22v__shw_g',
                b'c_xm22v__sw_g', b'c_xm8__kw_g', b'c_xm8__sfw_g', b'c_xm8__shw_g', b'c_xm8__sw_g', b'c_xm8c__kw_g',
                b'c_xm8c__sfw_g', b'c_xm8c__shw_g', b'c_xm8c__sw_g', b'c_xm8lmg__kw_g', b'c_xm8lmg__sfw_g',
                b'c_xm8lmg__shw_g', b'c_xm8lmg__sw_g', b'deaths', b'dogr', b'dogt', b'dp03_00', b'dp03_01', b'dp04_00',
                b'dp04_01', b'dp07_00', b'dp07_01', b'dp08_00', b'dp08_01', b'dta03_00', b'dta03_01', b'dta04_00',
                b'dta04_01', b'elo', b'elo0', b'elo1', b'form', b'games', b'hac_00', b'hac_01', b'hav_00', b'hav_01',
                b'haw_00', b'haw_01', b'hvb_00', b'hvb_01', b'hwb_00', b'hwb_01', b'kills', b'losses', b'rank',
                b'sc_assault', b'sc_award', b'sc_bonus', b'sc_demo', b'sc_general', b'sc_objective', b'sc_recon',
                b'sc_squad', b'sc_support', b'sc_team', b'sc_vehicle', b'score', b'teamkills', b'time', b'veteran',
                b'wins'],
    'minimal': [b'accuracy', b'c___h_g', b'c___r_g', b'c___res_g', b'c___rev_g', b'deaths', b'dogr', b'dogt', b'elo',
                b'elo0', b'elo1', b'form', b'games', b'kills', b'losses', b'rank', b'sc_assault', b'sc_award',
                b'sc_bonus', b'sc_demo', b'sc_general', b'sc_objective', b'sc_recon', b'sc_squad', b'sc_support',
                b'sc_team', b'sc_vehicle', b'score', b'teamkills', b'time', b'veteran', b'wins'],
    'weapons': [b'c_40mmgl__kw_g', b'c_40mmgl__sfw_g', b'c_40mmgl__shw_g', b'c_40mmgl__sw_g', b'c_40mmsg__kw_g',
                b'c_40mmsg__sfw_g', b'c_40mmsg__shw_g', b'c_40mmsg__sw_g', b'c_9a91__kw_g', b'c_9a91__sfw_g',
                b'c_9a91__shw_g', b'c_9a91__sw_g', b'c__40mmgl_hsh_g', b'c__40mmsg_hsh_g', b'c__9a91_hsh_g',
                b'c__aaw_hsh_g', b'c__aek_hsh_g', b'c__ak47v_hsh_g', b'c__aks74u_hsh_g', b'c__an94_hsh_g',
                b'c__aug_hsh_g', b'c__boaw_hsh_g', b'c__defi_hsh_g', b'c__f2000_hsh_g', b'c__g3_hsh_g', b'c__gol_hsh_g',
                b'c__helw_hsh_g', b'c__m16_hsh_g', b'c__m16a1v_hsh_g', b'c__m16k_hsh_g', b'c__m1911_hsh_g',
                b'c__m1_hsh_g', b'c__m1a1_hsh_g', b'c__m21v_hsh_g', b'c__m249_hsh_g', b'c__m24_hsh_g', b'c__m2v_hsh_g',
                b'c__m40v_hsh_g', b'c__m416_hsh_g', b'c__m60_hsh_g', b'c__m60v_hsh_g', b'c__m93r_hsh_g',
                b'c__m95_hsh_g', b'c__m95k_hsh_g', b'c__m9_hsh_g', b'c__mac10v_hsh_g', b'c__mcs_hsh_g',
                b'c__mg36_hsh_g', b'c__mg3_hsh_g', b'c__mg3k_hsh_g', b'c__mk14ebr_hsh_g', b'c__mp412_hsh_g',
                b'c__n2k_hsh_g', b'c__pkm_hsh_g', b'c__pp2_hsh_g', b'c__ppshv_hsh_g', b'c__prtg_hsh_g',
                b'c__qbu88_hsh_g', b'c__qju88_hsh_g', b'c__rept_hsh_g', b'c__rpkv_hsh_g', b'c__s12k_hsh_g',
                b'c__scar_hsh_g', b'c__smol_hsh_g', b'c__spas12_hsh_g', b'c__stgl_hsh_g', b'c__stmg_hsh_g',
                b'c__sv98_hsh_g', b'c__svdv_hsh_g', b'c__svu_hsh_g', b'c__tanc_hsh_g', b'c__tanm_hsh_g',
                b'c__tt33v_hsh_g', b'c__u12_hsh_g', b'c__ump_hsh_g', b'c__umpk_hsh_g', b'c__uzi_hsh_g', b'c__vss_hsh_g',
                b'c__xm22v_hsh_g', b'c__xm8_hsh_g', b'c__xm8c_hsh_g', b'c__xm8lmg_hsh_g', b'c_aek__kw_g',
                b'c_aek__sfw_g', b'c_aek__shw_g', b'c_aek__sw_g', b'c_ak47v__kw_g', b'c_ak47v__sfw_g',
                b'c_ak47v__shw_g', b'c_ak47v__sw_g', b'c_aks74u__kw_g', b'c_aks74u__sfw_g', b'c_aks74u__shw_g',
                b'c_aks74u__sw_g', b'c_an94__kw_g', b'c_an94__sfw_g', b'c_an94__shw_g', b'c_an94__sw_g', b'c_atm__kw_g',
                b'c_atm__sfw_g', b'c_atm__shw_g', b'c_atm__sw_g', b'c_aug__kw_g', b'c_aug__sfw_g', b'c_aug__shw_g',
                b'c_aug__sw_g', b'c_c4__kw_g', b'c_c4__sfw_g', b'c_c4__shw_g', b'c_c4__sw_g', b'c_defi__kw_g',
                b'c_defi__sfw_g', b'c_defi__shw_g', b'c_defi__sw_g', b'c_f2000__kw_g', b'c_f2000__sfw_g',
                b'c_f2000__shw_g', b'c_f2000__sw_g', b'c_g3__kw_g', b'c_g3__sfw_g', b'c_g3__shw_g', b'c_g3__sw_g',
                b'c_gol__kw_g', b'c_gol__sfw_g', b'c_gol__shw_g', b'c_gol__sw_g', b'c_helw__kw_g', b'c_hgr__kw_g',
                b'c_hgr__sfw_g', b'c_hgr__shw_g', b'c_hgr__sw_g', b'c_knv__kw_g', b'c_knv__sfw_g', b'c_knv__shw_g',
                b'c_knv__sw_g', b'c_m136__kw_g', b'c_m136__sfw_g', b'c_m136__shw_g', b'c_m136__sw_g', b'c_m14v__sw_g',
                b'c_m16__kw_g', b'c_m16__sfw_g', b'c_m16__shw_g', b'c_m16__sw_g', b'c_m16a1v__kw_g', b'c_m16a1v__sfw_g',
                b'c_m16a1v__shw_g', b'c_m16a1v__sw_g', b'c_m16k__kw_g', b'c_m16k__sfw_g', b'c_m16k__shw_g',
                b'c_m16k__sw_g', b'c_m1911__kw_g', b'c_m1911__sfw_g', b'c_m1911__shw_g', b'c_m1911__sw_g',
                b'c_m1__kw_g', b'c_m1__sfw_g', b'c_m1__shw_g', b'c_m1__sw_g', b'c_m1a1__kw_g', b'c_m1a1__sfw_g',
                b'c_m1a1__shw_g', b'c_m1a1__sw_g', b'c_m21v__kw_g', b'c_m21v__sfw_g', b'c_m21v__shw_g', b'c_m21v__sw_g',
                b'c_m249__kw_g', b'c_m249__sfw_g', b'c_m249__shw_g', b'c_m249__sw_g', b'c_m24__kw_g', b'c_m24__sfw_g',
                b'c_m24__shw_g', b'c_m24__sw_g', b'c_m2cg__kw_g', b'c_m2cg__sfw_g', b'c_m2cg__shw_g', b'c_m2cg__sw_g',
                b'c_m2v__kw_g', b'c_m2v__sfw_g', b'c_m2v__shw_g', b'c_m2v__sw_g', b'c_m40v__kw_g', b'c_m40v__sfw_g',
                b'c_m40v__shw_g', b'c_m40v__sw_g', b'c_m416__kw_g', b'c_m416__sfw_g', b'c_m416__shw_g', b'c_m416__sw_g',
                b'c_m60__kw_g', b'c_m60__sfw_g', b'c_m60__shw_g', b'c_m60__sw_g', b'c_m60v__kw_g', b'c_m60v__sfw_g',
                b'c_m60v__shw_g', b'c_m60v__sw_g', b'c_m93r__kw_g', b'c_m93r__sfw_g', b'c_m93r__shw_g', b'c_m93r__sw_g',
                b'c_m95__kw_g', b'c_m95__sfw_g', b'c_m95__shw_g', b'c_m95__sw_g', b'c_m95k__kw_g', b'c_m95k__sfw_g',
                b'c_m95k__shw_g', b'c_m95k__sw_g', b'c_m9__kw_g', b'c_m9__sfw_g', b'c_m9__shw_g', b'c_m9__sw_g',
                b'c_mac10v__kw_g', b'c_mac10v__sfw_g', b'c_mac10v__shw_g', b'c_mac10v__sw_g', b'c_mcs__kw_g',
                b'c_mcs__sfw_g', b'c_mcs__shw_g', b'c_mcs__sw_g', b'c_mg36__kw_g', b'c_mg36__sfw_g', b'c_mg36__shw_g',
                b'c_mg36__sw_g', b'c_mg3__kw_g', b'c_mg3__sfw_g', b'c_mg3__shw_g', b'c_mg3__sw_g', b'c_mg3k__kw_g',
                b'c_mg3k__sfw_g', b'c_mg3k__shw_g', b'c_mg3k__sw_g', b'c_mk14ebr__kw_g', b'c_mk14ebr__sfw_g',
                b'c_mk14ebr__shw_g', b'c_mk14ebr__sw_g', b'c_mots__kw_g', b'c_mots__sfw_g', b'c_mots__shw_g',
                b'c_mots__sw_g', b'c_mp412__kw_g', b'c_mp412__sfw_g', b'c_mp412__shw_g', b'c_mp412__sw_g',
                b'c_mp443__sfw_g', b'c_mp443__shw_g', b'c_mp443__sw_g', b'c_mst__kw_g', b'c_mst__sfw_g',
                b'c_mst__shw_g', b'c_mst__sw_g', b'c_n2k__kw_g', b'c_n2k__sfw_g', b'c_n2k__shw_g', b'c_n2k__sw_g',
                b'c_pkm__kw_g', b'c_pkm__sfw_g', b'c_pkm__shw_g', b'c_pkm__sw_g', b'c_pp2__kw_g', b'c_pp2__sfw_g',
                b'c_pp2__shw_g', b'c_pp2__sw_g', b'c_ppshv__kw_g', b'c_ppshv__sfw_g', b'c_ppshv__shw_g',
                b'c_ppshv__sw_g', b'c_qbu88__kw_g', b'c_qbu88__sfw_g', b'c_qbu88__shw_g', b'c_qbu88__sw_g',
                b'c_qju88__kw_g', b'c_qju88__sfw_g', b'c_qju88__shw_g', b'c_qju88__sw_g', b'c_rept__kw_g',
                b'c_rept__sfw_g', b'c_rept__shw_g', b'c_rept__sw_g', b'c_rpg7__kw_g', b'c_rpg7__sfw_g',
                b'c_rpg7__shw_g', b'c_rpg7__sw_g', b'c_rpkv__kw_g', b'c_rpkv__sfw_g', b'c_rpkv__shw_g', b'c_rpkv__sw_g',
                b'c_s12k__kw_g', b'c_s12k__sfw_g', b'c_s12k__shw_g', b'c_s12k__sw_g', b'c_scar__kw_g', b'c_scar__sfw_g',
                b'c_scar__shw_g', b'c_scar__sw_g', b'c_smol__kw_g', b'c_smol__sfw_g', b'c_smol__shw_g', b'c_smol__sw_g',
                b'c_spas12__kw_g', b'c_spas12__sfw_g', b'c_spas12__shw_g', b'c_spas12__sw_g', b'c_sv98__kw_g',
                b'c_sv98__sfw_g', b'c_sv98__shw_g', b'c_sv98__sw_g', b'c_svdv__kw_g', b'c_svdv__sfw_g',
                b'c_svdv__shw_g', b'c_svdv__sw_g', b'c_svu__kw_g', b'c_svu__sfw_g', b'c_svu__shw_g', b'c_svu__sw_g',
                b'c_trad__sfw_g', b'c_trad__sw_g', b'c_tt33v__kw_g', b'c_tt33v__sfw_g', b'c_tt33v__shw_g',
                b'c_tt33v__sw_g', b'c_u12__kw_g', b'c_u12__sfw_g', b'c_u12__shw_g', b'c_u12__sw_g', b'c_ump__kw_g',
                b'c_ump__sfw_g', b'c_ump__shw_g', b'c_ump__sw_g', b'c_umpk__kw_g', b'c_umpk__sfw_g', b'c_umpk__shw_g',
                b'c_umpk__sw_g', b'c_uzi__kw_g', b'c_uzi__sfw_g', b'c_uzi__shw_g', b'c_uzi__sw_g', b'c_uziv__sfw_g',
                b'c_uziv__sw_g', b'c_vss__kw_g', b'c_vss__sfw_g', b'c_vss__shw_g', b'c_vss__sw_g', b'c_xm22v__kw_g',
                b'c_xm22v__sfw_g', b'c_xm22v__shw_g', b'c_xm22v__sw_g', b'c_xm8__kw_g', b'c_xm8__sfw_g',
                b'c_xm8__shw_g', b'c_xm8__sw_g', b'c_xm8c__kw_g', b'c_xm8c__sfw_g', b'c_xm8c__shw_g', b'c_xm8c__sw_g',
                b'c_xm8lmg__kw_g', b'c_xm8lmg__sfw_g', b'c_xm8lmg__shw_g', b'c_xm8lmg__sw_g'],
    'vehicles': [b'c_KORD__si_g', b'c_KORN__si_g', b'c_MI28__ddw_g', b'c_MI28__si_g', b'c_PBLB__ddw_g', b'c_PBLB__si_g',
                 b'c_QLZ8__si_g', b'c_TOW2__si_g', b'c_VADS__si_g', b'c_XM307__si_g', b'c_XM312__si_g', b'c__KORD_ki_g',
                 b'c__KORN_ki_g', b'c__MI28_ki_g', b'c__PBLB_ki_g', b'c__QLZ8_ki_g', b'c__TOW2_ki_g', b'c__VADS_ki_g',
                 b'c__XM307_ki_g', b'c__XM312_ki_g', b'c__aav_ki_g', b'c__ah60_ki_g', b'c__ah64_ki_g', b'c__bmd3_ki_g',
                 b'c__bmda_ki_g', b'c__cav_ki_g', b'c__cobr_ki_g', b'c__gaz69v_ki_g', b'c__havoc_ki_g', b'c__hmv_ki_g',
                 b'c__hueyv_ki_g', b'c__jets_ki_g', b'c__m15v_ki_g', b'c__m1a2_ki_g', b'c__m3a3_ki_g', b'c__m48v_ki_g',
                 b'c__pbrv_ki_g', b'c__quad_ki_g', b'c__t54v_ki_g', b'c__t90_ki_g', b'c__uav_ki_g', b'c__vodn_ki_g',
                 b'c_aav__si_g', b'c_ah60__ddw_g', b'c_ah60__si_g', b'c_ah64__ddw_g', b'c_ah64__si_g', b'c_bmd3__ddw_g',
                 b'c_bmd3__si_g', b'c_bmda__ddw_g', b'c_bmda__si_g', b'c_cav__ddw_g', b'c_cav__si_g', b'c_cobr__ddw_g',
                 b'c_cobr__si_g', b'c_gaz69v__ddw_g', b'c_gaz69v__si_g', b'c_havoc__ddw_g', b'c_havoc__si_g',
                 b'c_hmv__ddw_g', b'c_hmv__si_g', b'c_hueyv__ddw_g', b'c_hueyv__si_g', b'c_jets__ddw_g',
                 b'c_jets__si_g', b'c_kuro__ddw_g', b'c_kuro__si_g', b'c_m15v__ddw_g', b'c_m15v__si_g',
                 b'c_m1a2__ddw_g', b'c_m1a2__si_g', b'c_m3a3__ddw_g', b'c_m3a3__si_g', b'c_m48v__ddw_g',
                 b'c_m48v__si_g', b'c_minitruckv__ddw_g', b'c_minitruckv__si_g', b'c_pbrv__ddw_g', b'c_pbrv__si_g',
                 b'c_quad__ddw_g', b'c_quad__si_g', b'c_rok_MI28_kwi_g', b'c_rok_PBLB_kwi_g', b'c_rok_ah60_kwi_g',
                 b'c_rok_ah64_kwi_g', b'c_rok_bmd3_kwi_g', b'c_rok_bmda_kwi_g', b'c_rok_cav_kwi_g',
                 b'c_rok_havoc_kwi_g', b'c_rok_hmv_kwi_g', b'c_rok_m15v_kwi_g', b'c_rok_m1a2_kwi_g',
                 b'c_rok_m3a3_kwi_g', b'c_rok_m48v_kwi_g', b'c_rok_quad_kwi_g', b'c_rok_t54v_kwi_g', b'c_rok_t90_kwi_g',
                 b'c_rok_uav_kwi_g', b'c_rok_vodn_kwi_g', b'c_t54v__ddw_g', b'c_t54v__si_g', b'c_t90__ddw_g',
                 b'c_t90__si_g', b'c_ta41_rok_heli_kwi_g', b'c_tru__ddw_g', b'c_tru__si_g', b'c_uav__ddw_g',
                 b'c_uav__si_g', b'c_vodn__ddw_g', b'c_vodn__si_g', b'c_vta04__gaz69v_ki_g', b'c_vta04__hueyv_ki_g',
                 b'c_vta04__m15v_ki_g', b'c_vta04__m48v_ki_g', b'c_vta04__pbrv_ki_g', b'c_vta04__t54v_ki_g',
                 b'c_vta05__tankv_ki_g', b'c_vta06__hueyv_ki_g']
}
MAINTAIN_PLAYER_IDS = {
    FeslPlatform.pc: 285735744,
    FeslPlatform.ps3: 273735378,
    FeslPlatform.xbox360: 201504424
}
THEATER_DIRTY_STR_KEYS = ['N', 'B-U-Time', 'B-U-PunkBusterVersion', 'D-BannerUrl', 'D-ServerDescription']
