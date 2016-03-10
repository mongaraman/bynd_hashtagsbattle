from django.contrib import admin

# Register your models here.
from .models import Battle

class BattleAdmin(admin.ModelAdmin):
    list_display = ["battle_id", "battle_name", "hashtag1", "hashtag2",
                    "battle_start", "battle_end"]
    list_display_link = ["battle_name"]
    #list_editable = ["battle_name"]
    ordering = ['battle_name']
    list_filter = ["battle_start", "battle_end", "timestamp", "updated"]
    search_fields = ["battle_name", "hashtag1", "hashtag2", "battle_start",
                    "battle_end"]
    class Meta:
        model = Battle

admin.site.register(Battle, BattleAdmin)



