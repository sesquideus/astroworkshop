#!/usr/bin/env python

import argparse
import yaml
import os
import sys
import jinja2
import dicts
import pprint


def environment(directory):
    env = jinja2.Environment(
        block_start_string='(@',
        block_end_string='@)',
        variable_start_string='(*',
        variable_end_string='*)',
        comment_start_string='(###',
        comment_end_string='###)',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        #undefined=jinja2.StrictUndefined,
        loader=jinja2.FileSystemLoader(directory),
    )
    return env


class Context():
    def __init__(self, data={}):
        self.data = data

    def add_dict(self, *args):
        self.data = dicts.merge(self.data, *args)
        return self

    def absorb_dict(self, key, ctx):
        self.data[key] = dicts.merge(self.data.get(key), ctx.data)
        return self

    def devour(self, context):
        self.data = dicts.merge(self.data, context.data)

    @classmethod
    def from_YAML(cls, file):
        try:
            contents = yaml.load(file, Loader=yaml.SafeLoader)
            contents = {} if contents is None else contents
        except FileNotFoundError as e:
            print(c.err("[FATAL] Could not load YAML file"), c.path(filename))
            raise e
        return cls(contents)

    def print(self):
        pprint.pprint(self.data)

    def __str__(self):
        return pprint.pformat(self.data)


class Builder():
    def __init__(self):
        argparser = argparse.ArgumentParser('Jinja builder')
        argparser.add_argument('input', type=argparse.FileType('r'))
        argparser.add_argument('-c', '--context', nargs=1, type=argparse.FileType('r'), action='append')
        argparser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
        argparser.add_argument('-d', '--debug', action='store_true')
        self.args = argparser.parse_args()
        self.env = environment('.')

    def load_context(self):
        self.context = Context()

        if self.args.context is not None:
            for context_file in self.args.context:
                self.context.devour(Context.from_YAML(context_file[0]))

            if self.args.debug:
                self.context.print()

    def build(self):
        print(
            self.env.get_template(self.args.input.name).render(self.context.data),
            file=self.args.output,
        )


builder = Builder()
builder.load_context()
builder.build()
