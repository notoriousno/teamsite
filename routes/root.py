from jinja2 import Environment
from klein import Klein
from twisted.internet import defer
from twisted.web.static import File


class Root(object):

    router = Klein()

    def __init__(self, jinja_env, db_pool):
        self.jinja_env = jinja_env
        self.db_pool = db_pool

    @router.route('/css', branch=True)
    def css_dir(self, request):
        return File('./public/css')

    @router.route('/images', branch=True)
    def image_dir(self, request):
        return File('./public/images')

    @router.route('/home', methods=['GET'])
    @defer.inlineCallbacks
    def homepage(self, request):
        limit = 4
        matches = yield self.db_pool.runQuery('''
            SELECT _id, opponent, our_score, their_score
            FROM match
        ''')
        team_record = win_loss_tie(matches)

        news = [
            "The Electric Eels are in search of a Graphic Artist to design new web page. Apply now!",
            "Heavy rainfall and thunder storms has delayed many games around the league.",
            "Fundraiser event will be held at the end of the month. Please bring family and friends!",
        ]
        if team_record[0] > team_record[1]:
            news.append("The Electric Eels finish the season strong! Our record is {0}-{1}-{2}.".format(*team_record))
        else:
            news.append("Better luck next year Electric Eels! Our record is {0}-{1}-{2}. Want to help us get better?".format(*team_record))

        template = self.jinja_env.get_template('homepage.html')
        return template.render(
            matches = matches[:limit],
            news = news)


def win_loss_tie(match_results):
    """
    :param match_results: [(_id, team, our_score, their_score), ...]
    :return: (win, loss, tie)
    """
    win = 0
    loss = 0
    tie = 0

    for _id, team, our_score, their_score in match_results:
        if our_score > their_score:
            win += 1
        elif our_score < their_score:
            loss += 1
        else:
            tie += 1

    return (win, loss, tie)

