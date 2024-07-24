from django.contrib import admin

from ..models import Affiliation


class AffiliationInline(admin.TabularInline):
    model = Affiliation
    extra = 1

    list_select_related = True


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ['person', 'institute', 'start', 'end']
    ordering = ['person', 'start']

    def get_queryset(self, request):
        return self.model.objects.prefetch_related('person', 'institute')
