using Application.SpecialDays.Commands.CreateSpecialDay;
using Application.SpecialDays.Commands.DeleteSpecialDay;
using Application.SpecialDays.Commands.UpdateSpecialDay;
using Application.SpecialDays.Queries.GetSpecialDay;
using Application.SpecialDays.Queries.GetSpecialDays;
using Microsoft.AspNetCore.Mvc;

namespace WebApi.Controllers;

public class SpecialDaysController : ApiControllerBase
{
    [HttpPost]
    public async Task<ActionResult> CreateSpecialDay(CreateSpecialDayCommand command)
    {
        var data = await Mediator.Send(command);
        return Ok(data);
    }

    [HttpPut]
    public async Task<ActionResult> UpdateSpecialDay(UpdateSpecialDayCommand command)
    {
        var data = await Mediator.Send(command);
        return Ok(data);
    }

    [HttpGet]
    public async Task<ActionResult> GetSpecialDays()
    {
        var data = await Mediator.Send(new GetSpecialDaysQuery());
        return Ok(data);
    }
    [HttpGet("{id}")]
    public async Task<ActionResult> GetSpecialDay(Guid id)
    {
        var data = await Mediator.Send(new GetSpecialDayQuery { Id = id });
        return Ok(data);
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult> DeleteSpecialDay(Guid id)
    {
        await Mediator.Send(new DeleteSpecialDayCommand { Id = id });
        return StatusCode(200);
    }
}
