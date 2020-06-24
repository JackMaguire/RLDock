from pyrosetta import *
from pyrosetta.teaching import *
#import rosetta.protocols.rigid as rigid_moves
from pyrosetta.rosetta.protocols.rosetta_scripts import *
from pyrosetta.rosetta.core.kinematics import Jump

pyrosetta.init( "-mute all" )
ft_tag = "<AtomTree fold_tree_file=\"test_aligned_3H.foldtree\" />"
ft_mover = XmlObjects.static_get_mover( ft_tag )

only_do_low_res = False

def magic_number_for_failed_docking_filter():
    return 1;

def magic_number_for_failed_design_filter():
    return 0.5;

def score_separate_dofs( t, r ):
    assert( len( t ) == 3 )
    assert( len( r ) == 3 )
    return score_dofs( [ t[0], t[1], t[2], r[0], r[1], r[2] ] )

def score_dofs( dofs ):
    assert( len( dofs ) == 6 )
    
    pose = pose_from_pdb("test_aligned_3H.pdb")   # input pdbfile
    #pose = pose_from_pdb("3u3b.clean.pdb")
    #pose = pose_from_sequence("VVV/LLLK")
    #return len(pose.chain_sequence( 1 ))

    # switch to centroid pose temporarily
    recover_sidechains = ReturnSidechainMover(pose)
    switch = SwitchResidueTypeSetMover("centroid")
    switch.apply(pose)

    #TODO setup foldtree
    #chain 1 has 117 residues
    #chain 2 has 18 residues
    #ft_tag = "<AtomTree fold_tree_file=\"test_aligned_3H.foldtree\" />"
    #ft_mover = XmlObjects.static_get_mover( ft_tag )
    ft_mover.apply( pose )
    pose.fold_tree().check_fold_tree()
    
    jump = Jump( pose.jump( pose.num_jump() ) )
    jump_control = Jump( pose.jump( pose.num_jump() ) )

    #ALL ANGLES ARE IN DEGREES
    
    T_factor = 10
    R_factor = 90
    new_tx = jump_control.get_rb_delta( 1, 1 ) + (dofs[ 0 ]*T_factor)
    new_ty = jump_control.get_rb_delta( 2, 1 ) + (dofs[ 1 ]*T_factor)
    new_tz = jump_control.get_rb_delta( 3, 1 ) + (dofs[ 2 ]*T_factor)
    new_rx = jump_control.get_rb_delta( 4, 1 ) + (dofs[ 3 ]*R_factor)
    new_ry = jump_control.get_rb_delta( 5, 1 ) + (dofs[ 4 ]*R_factor)
    new_rz = jump_control.get_rb_delta( 6, 1 ) + (dofs[ 5 ]*R_factor)
    
    #jump.set_rb_delta(Jump::ROT_X, 1, numeric::random::gaussian() * magnitude_rotation());
    jump.set_rb_delta( 1, 1, new_tx )
    jump.set_rb_delta( 2, 1, new_ty )
    jump.set_rb_delta( 3, 1, new_tz )
    jump.set_rb_delta( 4, 1, new_rx )
    jump.set_rb_delta( 5, 1, new_ry )
    jump.set_rb_delta( 6, 1, new_rz )
    
    #Perform quick filter
    low_res_sfxn = create_score_function( "interchain_cen" )
    low_res_sfxn.set_weight(interchain_contact, 4.0 )
    low_res_sfxn.set_weight(interchain_pair, 0.0 )
    low_res_sfxn.set_weight(interchain_env, 0.0 )

    #Make the chains go very far away
    jump_control.set_rb_delta( 1, 1, 1000 )
    pose.set_jump( pose.num_jump(), jump_control )
    low_res_control = low_res_sfxn.score( pose )

    pose.set_jump( pose.num_jump(), jump )
    low_res_score = low_res_sfxn.score( pose ) - low_res_control

    # TODO
    if only_do_low_res:
        return low_res_score / 10 #TEMP

    print( "low_res_score", low_res_score )
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
