from django.contrib import admin

import core

# Register your models here.

@admin.register(core.models.Institute)
class InstitudeAdmin(admin.ModelAdmin):
    pass


class AffiliationInline(admin.TabularInline):
    model = core.models.Affiliation


@admin.register(core.models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline]


@admin.register(core.models.Talk)
class TalkAdmin(admin.ModelAdmin):
    pass

@admin.register(core.models.Participation)
class ParticipationAdmin(admin.ModelAdmin):
    pass

@admin.register(core.models.Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(core.models.Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass
