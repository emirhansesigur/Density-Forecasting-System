using MediatR;
using Microsoft.EntityFrameworkCore;
using Persistence;

namespace Application.SpecialDays.Commands.DeleteSpecialDay;
public class DeleteSpecialDayCommand : IRequest
{
    public Guid Id { get; set; }
}

public class DeleteSpecialDayCommandHandler(ApplicationDbContext context) : IRequestHandler<DeleteSpecialDayCommand>
{
    public async Task Handle(DeleteSpecialDayCommand request, CancellationToken cancellationToken)
    {
        var entity = await context.Set<Domain.Entities.SpecialDay>().FirstOrDefaultAsync(x => x.Id == request.Id, cancellationToken: cancellationToken)
           ?? throw new KeyNotFoundException($"SpecialDay with Id {request.Id} not found.");

        context.Set<Domain.Entities.SpecialDay>().Remove(entity);
        await context.SaveChangesAsync(cancellationToken);
    }
}
