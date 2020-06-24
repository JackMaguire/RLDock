from pyrosetta import *
from pyrosetta.teaching import *
import rosetta.protocols.rigid as rigid_moves
from rosetta.protocols.rosetta_scripts import *

def magic_number_for_failed_docking_filter():
    return 1;

def magic_number_for_failed_design_filter():
    return 0.5;

def score_dofs( dofs ):

    assert( len( dofs ) == 6 )
    
    pose = pose_from_pdb("test_aligned_3H.pdb")   # input pdbfile

    # switch to centroid pose temporarily
    recover_sidechains = ReturnSidechainMover(pose)
    switch = SwitchResidueTypeSetMover("centroid")
    switch.apply(pose)

    #TODO setup foldtree
    
    
    jump = pose.jump( pose.num_jumps() )

    #ALL ANGLES ARE IN DEGREES
    
    T_factor = 10
    R_factor = 180
    d_tx = dofs[ 0 ] * T_factor
    d_ty = dofs[ 1 ] * T_factor
    d_tz = dofs[ 2 ] * T_factor
    d_rx = dofs[ 3 ] * R_factor
    d_ry = dofs[ 4 ] * R_factor
    d_rz = dofs[ 5 ] * R_factor
    
    #jump.set_rb_delta(Jump::ROT_X, 1, numeric::random::gaussian() * magnitude_rotation());
    jump.set_rb_delta( rosetta.core.kinematics.Jump.TRANS_X, 1, d_tx )
    jump.set_rb_delta( rosetta.core.kinematics.Jump.TRANS_Y, 1, d_ty )
    jump.set_rb_delta( rosetta.core.kinematics.Jump.TRANS_Z, 1, d_tz )
    jump.set_rb_delta( rosetta.core.kinematics.Jump.ROT_X, 1, d_rx )
    jump.set_rb_delta( rosetta.core.kinematics.Jump.ROT_Y, 1, d_ry )
    jump.set_rb_delta( rosetta.core.kinematics.Jump.ROT_Z, 1, d_rz )

    #Perform quick filter
    low_res_sfxn = create_score_function( "interchain_cen" )
    low_res_sfxn.set_weight(interchain_contact, 4.0 )
    low_res_sfxn.set_weight(interchain_pair, 0.0 )
    low_res_sfxn.set_weight(interchain_env, 0.0 )
    low_res_score = low_res_sfxn.score( pose )
    if low_res_score >= 0.0:
        return magic_number_for_failed_docking_filter()

    #Go back into high-resolution mode
    switch2 = SwitchResidueTypeSetMover( "fa_standard" )
    switch2.apply( pose )
    recover_sidechains.apply( pose )

    #Perform Design
    parser = RosettaScriptsParser()
    protocol = parser.generate_mover( "design.xml" )
    protocol.apply( pose )

    if protocol.get_last_move_status() != protocols.moves.MS_SUCCESS:
        return magic_number_for_failed_design_filter()

    sfxn = create_score_function( "ref2015" )
    final_score_per_residue = sfxn.score( pose ) / pose.size()
    #We expect final_score_per_residue to be in the -3 to -2 range
    #We want it to be in the -1 to 0 range
    normalized_score_per_residue = final_score_per_residue + 2
    if normalized_score_per_residue > magic_number_for_failed_design_filter():
        #We don't want to punish the trajectory for passing filters
        return magic_number_for_failed_design_filter()
    return normalized_score_per_residue
