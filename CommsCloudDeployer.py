#!/usr/bin/env python

import argparse
import sys
import os
import resources.git_handler as git_handler
import resources.cc_handler as cc_handler
import resources.printcolors as clr
from settings import MANIFEST_ONLY, TAG_PREFIX, BASE_DIR


def add_args():
    parser = argparse.ArgumentParser(
        prog='Comms Cloud Deployer',
        description='Generate .yaml file with manifest files to deploy',
    )

    parser.add_argument("-b", "--branch",
                        help="Name of the branch",
                        required=True)
    parser.add_argument("-o", "--org",
                        help="Name of the target Org",
                        required=True)
    parser.add_argument("-c", "--catalog",
                        help="Name of the catalog for Communications Cloud data",
                        required=True)
    parser.add_argument("-t", "--tagOnly",
                        help="Create only the new tag",
                        required=True)

    return parser


def get_args(parser) -> dict:
    result_args = {}
    args = parser.parse_args()
    result_args['branch'] = args.branch
    result_args['catalog'] = args.catalog
    result_args['org'] = args.org
    result_args['tagOnly'] = args.tagOnly

    return result_args

def skip_manifest(args, manifest_only):
    clr.print_info("Skipping generating dynamic manifest file")
    cc_handler.write_changes_to_yaml("", args['catalog'], manifest_only)


def main():
    parser = add_args()
    args = get_args(parser)  # get arguments from user command input

    clr.print_info('Manifest only setup: ' + str(MANIFEST_ONLY))
    clr.print_info('Working path: ' + str(BASE_DIR))
    clr.print_line()

    if args['tagOnly'].capitalize() == 'Y':
        clr.print_info("Creating new tag")
        new_tag = git_handler.add_tag_with_prefix(args['org'])
        if not new_tag:
            clr.print_error("Failed to create new tag")
        clr.print_success('Script ended')
        return

    if not MANIFEST_ONLY:  # Skip generating dynamic manifest if MANIFEST_ONLY is set up to False
        skip_manifest(args, False)
    clr.print_info('Retrieving last tag')
    last_tag = git_handler.get_last_tag_with_prefix(args['branch'], args['org'])
    if last_tag is not None:
        clr.print_success(f"Latest tag was found on the '{args['branch']}' branch: {last_tag}):")
        print(type(last_tag))
        clr.print_info('Retrieving diff changes since last tag')
        changes = git_handler.get_changes_since_last_tag(last_tag, args['catalog'])

        if not changes or changes[0] == '':
            clr.print_info(f"There are no changes on '{args['branch']}' branch since the last tag.")
            skip_manifest(args, True)
        else:
            clr.print_success(f"Changes inside '{args['catalog']}' catalog on the '{args['branch']}' branch since the last tag:")
            for change in changes:
                if change:  # Skip empty lines
                    clr.print_info(" - " + change)

            clr.print_info("Generating manifest changes")
            manifest_changes = cc_handler.get_comms_cloud_paths(changes, args['catalog'])
            print(manifest_changes)
            if len(manifest_changes) > 0:
                clr.print_info("Writing changes to yaml file")
                cc_handler.write_changes_to_yaml(manifest_changes, args['catalog'], True)


    else:
        clr.print_info(f"There is no existing tag with prefix '{TAG_PREFIX}{args['branch']}'")
        skip_manifest(args, False)



    clr.print_success('Script ended')
    clr.print_line()


if __name__ == '__main__':
    main()
