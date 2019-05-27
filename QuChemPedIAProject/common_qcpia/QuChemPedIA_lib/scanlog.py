#!/usr/bin/python3 -W ignore
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import json
import pickle
import hashlib
import traceback

import cclib  # custom github BenoitDamota/cclib (clone+pythonpath)
import pybel  # included in openbabel (pip install open babel)
import numpy as np
import openbabel as ob  # (apt + pip)
import scipy.sparse as sp
import sklearn.preprocessing

# constants
CstBohr2Ang = 0.52917721092
CstHartree2eV = 27.21138505
CstHartree2cm1 = 219474.6313708
scanlog_version = "v7.4a"

""" Scanlog Exception class.
"""


class ScanlogException(Exception):
    pass


"""Redefining nuclear_repulsion_energy with 5 decimals of precision on coords.
"""


def nuclear_repulsion_energy(data, slice_id=-1):
    nre = 0.0
    for i in range(data.natom):
        ri = np.array([float("%.5f" % k) for k in data.atomcoords[slice_id][i]])
        zi = data.atomnos[i]
        for j in range(i + 1, data.natom):
            rj = np.array([float("%.5f" % k) for k in data.atomcoords[slice_id][j]])
            zj = data.atomnos[j]
            d = np.linalg.norm(ri - rj)
            nre += zi * zj / d
    return float("%.5f" % (nre * CstBohr2Ang))


"""Utility function to simplify data recording from dict or other object.
"""


def _try_key_insertion(res_json, key, obj, obj_path=[], nullable=True):
    # case : dictionary
    if obj.__class__ == dict:
        try:
            if obj_path:
                d = obj.copy()
                for k in obj_path:
                    d = d[k]
                res_json[key] = d
        except Exception as e:
            if not nullable:
                raise ScanlogException("Fatal : error occured for required key %s" % key)
            # else error occured but key is not required
    # case : simple object
    elif obj != 'N/A':
        res_json[key] = obj
    elif not nullable:
        raise ScanlogException("Fatal : key %s is N/A but is required" % key)
    # else obj is 'N/A' ans is ignored


def general_param_subsection(res_json, data_json, data, obdata):
    res_json["comp_details"]["general"] = {}
    section = res_json["comp_details"]["general"]

    try:
        all_unique_theory = np.unique(data.metadata['methods'])
        if len(all_unique_theory) > 1:
            theo_array = np.array(data.metadata['methods'])
            _, theo_indices = np.unique(theo_array, return_index=True)
            theo_indices.sort()
            theo_array = theo_array[theo_indices]
        else:
            theo_array = all_unique_theory
    except:
        theo_array = 'N/A'
    if theo_array.__class__ != str:
        if len(theo_array) > 0:
            theo_array = theo_array.tolist() if (theo_array != 'N/A').any() else 'N/A'
        else:
            theo_array = 'N/A'
    if len(all_unique_theory) > 0:
        all_unique_theory = all_unique_theory.tolist() if (all_unique_theory != 'N/A').any() else 'N/A'
    else:
        all_unique_theory = 'N/A'
    methods = data.metadata.get('methods', ['N/A'])

    _try_key_insertion(section, "package", data.metadata, ['package'])
    _try_key_insertion(section, "package_version", data.metadata, ['package_version'])
    _try_key_insertion(section, "all_unique_theory", all_unique_theory)
    if len(methods) > 0:
        _try_key_insertion(section, "last_theory", methods[-1])
    _try_key_insertion(section, "list_theory", theo_array)
    _try_key_insertion(section, "functional", data.metadata, ['functional'])
    _try_key_insertion(section, "basis_set_name", data.metadata, ['basis_set'])
    # basis set Pickle version
    try:
        basis_str = pickle.dumps(data.gbasis, protocol=0)
        basis_hash = hashlib.md5(basis_str).hexdigest()
        _try_key_insertion(section, "basis_set", basis_str.decode())  # "%s"  % basis_str[2:-1])
        _try_key_insertion(section, "basis_set_md5", basis_hash)
    except:
        pass
    _try_key_insertion(section, "basis_set_size", data_json, ['properties', 'orbitals', 'basis number'])
    _try_key_insertion(section, "ao_names", data_json, ['atoms', 'orbitals', 'names'])
    try:
        section["is_closed_shell"] = repr(len(data.moenergies) == 1
                                          or np.allclose(*data.moenergies, atol=1e-6))
    except:
        pass
    _try_key_insertion(section, "integration_grid", data_json, ['properties', 'integration grid'])
    _try_key_insertion(section, "solvent", data.metadata, ['solvent'])
    _try_key_insertion(section, "solvent_reaction_field", data.metadata, ['scrf'])
    _try_key_insertion(section, "scf_targets", data_json, ['optimization', 'scf', 'targets'])
    _try_key_insertion(section, "core_electrons_per_atoms", data_json, ['atoms', 'core electrons'])


def geometry_param_subsection(res_json, data_json, data, obdata):
    res_json["comp_details"]["geometry"] = {}
    section = res_json["comp_details"]["geometry"]
    _try_key_insertion(section, "geometric_targets", data_json, ['optimization', 'geometric targets'])


def freq_param_subsection(res_json, data_json, data, obdata):
    res_json["comp_details"]["freq"] = {}
    section = res_json["comp_details"]["freq"]
    _try_key_insertion(section, "temperature", data_json, ['properties', 'temperature'])
    _try_key_insertion(section, "anharmonicity", data_json, ['vibrations', 'anharmonicity constants'])


def td_param_subsection(res_json, data_json, data, obdata):
    res_json["comp_details"]["excited_states"] = {}
    section = res_json["comp_details"]["excited_states"]

    et_states = data_json.get('transitions', {}).get('electronic transitions', None)
    if et_states:
        section["nb_et_states"] = len(et_states)
    ## TODO
    # res_json["comp_details"]["excited_states"]["TDA"] = 'N/A' # TODO : test Tamm Damcoff approx.
    # res_json["comp_details"]["excited_states"]["et_sym_constraints"] = 'N/A'
    # res_json["comp_details"]["excited_states"]["et_optimization"] = 'N/A' # boolean (if optimization of ES)
    # res_json["comp_details"]["excited_states"]["opt_root_number"] = 'N/A' # optimized ES number


def wavefunction_results_subsection(res_json, data_json, data, obdata):
    res_json["results"]["wavefunction"] = {}
    section = res_json["results"]["wavefunction"]

    _try_key_insertion(section, "homo_indexes", data_json, ['properties', 'orbitals', 'homos'])
    _try_key_insertion(section, "MO_energies", data_json, ['properties', 'orbitals', 'energies'])
    _try_key_insertion(section, "MO_sym", data_json, ['properties', 'orbitals', 'molecular orbital symmetry'])
    # MO_number, MO_energies, MO_sym, MO_coefs
    try:
        _try_key_insertion(section, "MO_number", data_json, ['properties', 'orbitals', 'MO number'],
                           nullable=False)  # not nullable in this context, exception catched.
        # TODO : Pb with energies, if NaN -> -inf
        data.moenergies[-1][np.isnan(data.moenergies[-1])] = -np.inf
        w_cut = np.where(data.moenergies[-1] > 10.)
        b_cut = min(max(w_cut[0][0] if len(w_cut[0]) > 0 else 0,
                        data.homos.max() + 31),
                    len(data.moenergies[-1]))
        _try_key_insertion(section, "MO_number_kept", int(b_cut))

        # prune energies and sym
        _try_key_insertion(section, "MO_energies", [moen[:b_cut] for moen in section["MO_energies"]])
        _try_key_insertion(section, "MO_sym", [mosym[:b_cut] for mosym in section["MO_sym"]])

        # compress and prune mocoeffs
        threshold = 0.05  # compression with loss threshold
        mo_coefs = []
        # take last mocoeffs  (-2 with alpha/beta or -1)
        nb_coef = -2 if len(data.moenergies) == 2 else -1
        for a in data.mocoeffs[nb_coef:]:
            # normalization
            a_ = sklearn.preprocessing.normalize(np.abs(a), norm='l1', copy=False)
            # indices of sorting and sorting
            a_argsort = a_.argsort(1)
            a_.sort(axis=1)
            # where are values under the threshold (based on cumsum)
            az = np.where(a_.cumsum(axis=1) < threshold)
            #  zeroing
            a[az[0], a_argsort[az]] = 0.
            a = a[:b_cut, :]
            # to sparse csr matrix
            acsr = sp.csr_matrix(a)
            # append tuple for the csr to mo_coefs
            mo_coefs.append((acsr.data.tolist(), acsr.indices.tolist(), acsr.indptr.tolist()))
        # data insertion into JSON
        section["MO_coefs"] = mo_coefs
    except Exception as e:
        # partial MO data (qc lvl2 takes the decision)
        pass
    _try_key_insertion(section, "total_molecular_energy", data_json, ['properties', 'energy', 'total'])
    # eV to Hartree conversion
    try:
        _try_key_insertion(section, "total_molecular_energy", section["total_molecular_energy"] / CstHartree2eV)
    except:
        ## TODO : pb with SP
        pass  # SP ? failure ?
    _try_key_insertion(section, "Mulliken_partial_charges", data_json, ['properties', 'partial charges', 'mulliken'])
    try:
        section["SCF_values"] = data_json['optimization']['scf']['values'][-1][-1]
    except:
        pass
    _try_key_insertion(section, "virial_ratio", data_json, ['optimization', 'scf', 'virialratio'])
    ## TODO # _try_key_insertion(section, "Hirshfeld_partial_charges"] = 'N/A' # see scanlog
    # try:
    #     section["Hirshfeld_partial_charges"] = data.atomcharges["hirshfeld"].tolist()
    # except:
    #     pass


def geom_results_subsection(res_json, data_json, data, obdata):
    res_json["results"]["geometry"] = {}
    section = res_json["results"]["geometry"]

    _try_key_insertion(section, "nuclear_repulsion_energy_from_xyz", nuclear_repulsion_energy(data))
    _try_key_insertion(section, "OPT_DONE", data_json, ['optimization', 'done'])
    _try_key_insertion(section, "elements_3D_coords_converged", data_json, ['atoms', 'coords', '3d'])
    _try_key_insertion(section, "geometric_values", data_json, ['optimization', 'geometric values'])


def freq_results_subsection(res_json, data_json, data, obdata):
    res_json["results"]["freq"] = {}
    section = res_json["results"]["freq"]

    _try_key_insertion(section, "entropy", data_json, ['properties', 'entropy'])
    try:
        _try_key_insertion(section, "entropy", float("%.9f" % section["entropy"]))
    except:
        pass
    _try_key_insertion(section, "enthalpy", data_json, ['properties', 'enthalpy'])
    _try_key_insertion(section, "free_energy", data_json, ['properties', 'energy', 'free energy'])
    _try_key_insertion(section, "zero_point_energy", data_json, ['properties', 'zero point energy'])
    _try_key_insertion(section, "electronic_thermal_energy", data_json, ['properties', 'electronic thermal energy'])
    try:
        section["polarizabilities"] = data.polarizabilities[0].tolist()
    except:
        pass
    _try_key_insertion(section, "vibrational_freq", data_json, ['vibrations', 'frequencies'])
    _try_key_insertion(section, "vibrational_int", data_json, ['vibrations', 'intensities', 'IR'])
    _try_key_insertion(section, "vibrational_sym", data_json, ['vibrations', 'vibration symmetry'])
    _try_key_insertion(section, "vibration_disp", data_json, ['vibrations', 'displacement'])
    _try_key_insertion(section, "vibrational_anharms", data_json, ['vibrations', 'anharmonicity constants'])
    _try_key_insertion(section, "vibrational_raman", data_json, ['vibrations', 'intensities', 'raman'])


def td_results_subsection(res_json, data_json, data, obdata):
    res_json["results"]["excited_states"] = {}
    section = res_json["results"]["excited_states"]

    _try_key_insertion(section, "et_energies", data_json, ['transitions', 'electronic transitions'])
    _try_key_insertion(section, "et_oscs", data_json, ['transitions', 'oscillator strength'])
    _try_key_insertion(section, "et_sym", data_json, ['transitions', 'symmetry'])
    _try_key_insertion(section, "et_rot", data_json, ['transitions', 'rotatory strength'])
    _try_key_insertion(section, "et_transitions", data_json, ['transitions', 'one excited config'])


def molecule_section(res_json, data_json, data, obdata, verbose=False):
    res_json["molecule"] = {}
    section = res_json["molecule"]

    # Start OpenBabel (all are mandatory)
    try:
        res_json["molecule"]["inchi"] = obdata.write("inchi").strip()  # remove trailing \n
        res_json["molecule"]["smi"] = obdata.write("smi").split()[0]
        res_json["molecule"]["can"] = obdata.write("can").split()[0]
        res_json["molecule"]["chirality"] = obdata.OBMol.IsChiral()
        res_json["molecule"]["monoisotopic_mass"] = obdata.OBMol.GetExactMass()  # in Dalton
        res_json["molecule"]["atoms_valence"] = [at.OBAtom.GetValence() for at in obdata.atoms]
        connectivity = {}
        connectivity["atom_pairs"] = []
        connectivity["bond_orders"] = []
        for i, a1 in enumerate(obdata.atoms):
            for j, a2 in enumerate(obdata.atoms):
                b = a1.OBAtom.GetBond(a2.OBAtom)
                if b is not None:
                    connectivity["atom_pairs"].append((i, j))
                    connectivity["bond_orders"].append(b.GetBondOrder())
        res_json["molecule"]["connectivity"] = connectivity
    except:
        if verbose:
            traceback.print_exc()
        raise ScanlogException("Reading mandatory data failed (Openbabel)")
    # End OpenBabel

    _try_key_insertion(section, "formula", data_json, ['formula'])
    # CRITICAL TODO formula versus inchi formula
    _try_key_insertion(section, "nb_atoms", data_json, ['properties', 'number of atoms'])
    _try_key_insertion(section, "nb_heavy_atoms", data_json, ['atoms', 'elements', 'heavy atom count'])
    _try_key_insertion(section, "charge", data_json, ['properties', 'charge'])
    _try_key_insertion(section, "multiplicity", data_json, ['properties', 'multiplicity'])
    _try_key_insertion(section, "atoms_Z", data_json, ['atoms', 'elements', 'number'])
    # _try_key_insertion(section, "atoms_masses", data.atommasses.tolist())
    # _try_key_insertion(section, "nuclear_spins", data.nuclearspins.tolist())
    # _try_key_insertion(section, "atoms_Zeff", data.atomzeff.tolist())
    # _try_key_insertion(section, "nuclear_QMom", data.nuclearqmom.tolist())
    # _try_key_insertion(section, "nuclear_gfactors", data.nucleargfactors.tolist())
    _try_key_insertion(section, "starting_geometry", data.atomcoords[0, :, :].tolist())
    ## TODO: pb with SP
    _try_key_insertion(section, "starting_energy", data_json,
                       ["optimization", "scf", "scf energies"])  # in eV
    try:
        # eV to Hartree conversion
        _try_key_insertion(section, "starting_energy", section["starting_energy"][0] / CstHartree2eV)
    except:
        pass  # SP ?
    _try_key_insertion(section, "starting_nuclear_repulsion", nuclear_repulsion_energy(data, 0))


def parameters_section(res_json, data_json, data, obdata):
    res_json["comp_details"] = {}
    # subsection : General parameters
    general_param_subsection(res_json, data_json, data, obdata)
    # subsection : Geometry
    geometry_param_subsection(res_json, data_json, data, obdata)
    # subsection : Thermochemistry and normal modes
    freq_param_subsection(res_json, data_json, data, obdata)
    # subsection :  Excited states
    td_param_subsection(res_json, data_json, data, obdata)


def results_section(res_json, data_json, data, obdata):
    res_json["results"] = {}
    # subsection : Wavefunction
    wavefunction_results_subsection(res_json, data_json, data, obdata)
    # subsection : Geometry
    geom_results_subsection(res_json, data_json, data, obdata)
    # subsection : Thermochemistry and normal modes
    freq_results_subsection(res_json, data_json, data, obdata)
    # subsection : Excited states
    td_results_subsection(res_json, data_json, data, obdata)


def metadata_section(logfile, res_json, data_json, data, obdata):
    res_json["metadata"] = {}
    section = res_json["metadata"]
    res_json["metadata"]["parser_version"] = scanlog_version
    res_json["metadata"]["log_file"] = os.path.basename(logfile)
    # res_json["metadata"]["publication_DOI"] = 'N/A'


def full_report(logfile, data_json, data, obdata, verbose=False):
    res_json = {}
    # section : Molecule
    molecule_section(res_json, data_json, data, obdata, verbose=verbose)
    # section : Computational details
    parameters_section(res_json, data_json, data, obdata)
    # section : Results
    results_section(res_json, data_json, data, obdata)
    # section : Metadata
    metadata_section(logfile, res_json, data_json, data, obdata)
    return res_json


def logfile_to_dict(logfile, verbose=False):
    # reading with cclib
    data = cclib.parser.ccopen(logfile).parse()
    data_json = json.loads(data.writejson())
    # openbabel sur XYZ
    obdata = pybel.readstring("xyz", data.writexyz())
    # construct new dict
    return full_report(logfile, data_json, data, obdata, verbose=verbose)


def job_type_guess(res_json):
    job_type = []
    # TODO : verify for other solvers
    if ((res_json["comp_details"]["general"]["package"] == "Gaussian") or
            (res_json["comp_details"]["general"]["package"] == "GAMESS")):
        ### TODO: GAMESS not tested, accepted here only for Riken DB insertion purpose (only OPT)
        ### Note: tested and works for TD
        if "vibrational_freq" in res_json["results"]["freq"].keys():
            if "nb_et_states" in res_json["comp_details"]["excited_states"].keys():
                job_type.append('FREQ_ES')
            else:
                job_type.append('FREQ')
        if "geometric_targets" in res_json["comp_details"]["geometry"].keys():  # problem with STO
            if "nb_et_states" in res_json["comp_details"]["excited_states"].keys():
                job_type.append('OPT_ES')
            else:
                job_type.append('OPT')
        elif "nb_et_states" in res_json["comp_details"]["excited_states"].keys():
            job_type.append('TD')
        if len(job_type) == 0:
            job_type.append('SP')
        # # un SP peut avoir des MO
        # if "MO_coefs" in res_json["results"]["wavefunction"].keys(): :
        #     job_type.append('MO')
    res_json["comp_details"]["general"]["job_type"] = job_type


"""Verify that Logfile is readable by cclib and extract solver.
"""


def quality_check_lvl1(logfile, verbose=False):
    if verbose:
        print(">>> START QC lvl1 <<<")
    try:
        # reading with cclib
        data = cclib.parser.ccopen(logfile).parse()
        if verbose:
            print("OK\n>>> END QC lvl1 <<<\n")
    except:
        raise ScanlogException("Quality check lvl1 failed : LOG file not readable (cclib failed on file %s)." % logfile)
    solver = data.metadata['package']
    return solver


"""Split Logfile.
"""


def split_logfile(logfile, solver, log_storage_path="", verbose=False):
    try:
        log_files = []
        # GAUSSIAN
        if verbose:
            print(">>> SOLVER:", solver)
        if solver == "Gaussian":
            TERM = "Normal termination"

            with open(logfile, 'r') as log_fd:
                lines = log_fd.readlines()
            nbl = len(lines)

            file_cnt = 0
            base_fname = os.path.basename(logfile).rsplit('.', 1)[0]
            log_pat = os.path.join(log_storage_path, "%s_step_%s.log" % (base_fname, "%d"))
            cur_log = log_pat % file_cnt
            if verbose:
                print(">>> Processing", cur_log, "...")
            cur_log_fd = open(cur_log, "w")
            # FLAG to add copyright at the beginning of each step.
            file_start = True

            for cur_l, line in enumerate(lines):
                if file_start:
                    cur_log_fd.write(" Copyright (c) 1988,1990,1992,1993,1995,1998,2003,2009,2013,\n")
                    cur_log_fd.write("            Gaussian, Inc.  All Rights Reserved.\n")
                    file_start = False

                cur_log_fd.write(line)
                if line.find(TERM) > -1:
                    file_start = True
                    if verbose:
                        print("=> ", line)
                    log_files.append(cur_log)
                    cur_log_fd.close()
                    file_cnt += 1
                    if nbl > (cur_l + 1):
                        cur_log = log_pat % file_cnt
                        if verbose:
                            print(">>> Processing", cur_log, "...")
                        cur_log_fd = open(cur_log, "w")
            if not cur_log_fd.closed:
                cur_log_fd.close()
        elif solver == "GAMESS":
            ### TODO : GAMESS not tested, accepted here only for Riken
            ### DB insertion purpose (only OPT mono step)
            TERM = "TERMINATED NORMALLY"
            with open(logfile, 'r') as log_fd:
                lines = log_fd.readlines()
            for line in lines:
                if line.find(TERM) > -1:
                    if verbose:
                        print("=> ", line)
                    log_files.append(logfile)
            pass
        else:  # other solvers
            log_files.append(logfile)
        if verbose:
            print(">>> Steps :", log_files, "\n")
        return log_files
    except:
        if verbose:
            traceback.print_exc()
        raise ScanlogException("File spliting failed.")


"""Check if logfile is archivable and candidate for a new entry.
"""


def quality_check_lvl2(res_json, solver, verbose=False):
    qual = "True"
    qual2 = "True"
    # if not "basis_set_md5" in res_json["comp_details"]["general"].keys():
    #     qual = "False"
    if not "total_molecular_energy" in res_json["results"]["wavefunction"].keys():
        qual = "False"
    # if OPT then res_json["results"]["wavefunction"]["MO_coefs"] needed
    # if 'OPT' in res_json["comp_details"]["general"]["job_type"]:
    #     if "MO_coefs" in res_json["results"]["wavefunction"].keys():
    #         qual2 = "True"
    # # If only OPT then qual = False (not archivable) ???
    # if len(res_json["comp_details"]["general"]["job_type"]) == 1:
    #     qual = "False"

    res_json['metadata']['archivable'] = qual
    res_json['metadata']['archivable_for_new_entry'] = qual2
    if verbose:
        print(">>> START QC lvl2 <<<")
        print("File:", res_json["metadata"]["log_file"])
        print("Job type:", res_json["comp_details"]["general"]["job_type"])
        print("Archivable:", res_json['metadata']['archivable'])
        print("Archivable for new entry:", res_json['metadata']['archivable_for_new_entry'])
        print(">>> END QC lvl2 <<<\n")


def process_logfile(logfile, log_storage_path="", verbose=False):
    solver = quality_check_lvl1(logfile, verbose=verbose)
    log_files = split_logfile(logfile, solver, log_storage_path=log_storage_path, verbose=verbose)
    json_list = []
    for log in log_files:
        res_json = logfile_to_dict(log, verbose=verbose)
        job_type_guess(res_json)
        quality_check_lvl2(res_json, solver, verbose=verbose)
        json_list.append(res_json)
    return (log_files, json_list)


def process_logfile_list(logfilelist, log_storage_path="", verbose=False):
    json_list = []
    log_files = []
    for logfile in logfilelist:
        l, j = process_logfile(logfile,
                               log_storage_path=log_storage_path,
                               verbose=verbose)
        json_list += j
        logfile += l

    return (log_files, json_list)


if __name__ == "__main__":
    log_files, json_list = process_logfile(sys.argv[1], log_storage_path="tmp", verbose=True)
    if len(sys.argv) == 3:
        with open(sys.argv[2], "w") as fp:
            json.dump(json_list, fp)
    else:
        print(">>> Processed successfully %d steps (over %d detected)." % (len(json_list),
                                                                           len(log_files)))
        print(json.dumps(json_list))
    # print(json_list)

