from django.forms import ModelForm
from gamedata.models import Game

class DeveloperGameForm(ModelForm):

	class Meta:
		model = Game
		fields = ['name', 'url', 'price', 'description', 'category', 'imageUrl']

	def save(self, commit=True):
		game = super(DeveloperGameForm, self).save(commit=False)

		if commit:
			game.save()
		return game