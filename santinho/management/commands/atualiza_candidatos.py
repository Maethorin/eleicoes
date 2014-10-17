# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "EH NOHIS"